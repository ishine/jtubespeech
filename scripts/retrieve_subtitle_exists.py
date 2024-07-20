import os
import time
import requests
import argparse
import re
import sys
import traceback
import subprocess
import shutil
import random
from pathlib import Path
from util import make_video_url, get_subtitle_language
import pandas as pd
from tqdm import tqdm
from torch.multiprocessing import Process, Queue

def parse_args():
  parser = argparse.ArgumentParser(
    description="Retrieving whether subtitles exists or not.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument("lang",         type=str, help="language code (ja, en, ...)")
  parser.add_argument("videoidlist",  type=str, help="filename of video ID list")  
  parser.add_argument("--outdir",     type=str, default="sub", help="dirname to save results")
  parser.add_argument("--checkpoint", type=str, default=None, help="filename of list checkpoint (for restart retrieving)")
  parser.add_argument("--proxies",    type=str, nargs='+', default="192.168.8.23:7890 192.168.8.123:7890 192.168.8.25:7890")
  return parser.parse_args(sys.argv[1:])

def retrieve_worker(proxy, lang, in_queue, out_queue, error_queue, error_vids, wait_sec):
  r = str(round(time.time()*1000)) + '_' + str(random.randint(10000000, 999999999))
  cookie_file = f'cookies_{r}.txt'
  shutil.copy('cookies.txt', cookie_file)
  for videoid in iter(in_queue.get, "STOP"):
    if videoid in error_vids:
      continue
    url = make_video_url(videoid)
    try:
      cmd = f"export http_proxy=http://{proxy} && export https_proxy=http://{proxy} && yt-dlp -v --cookies {cookie_file} --list-subs --sub-lang {lang} --skip-download {url}"
      #print(cmd)
      cp = subprocess.run(cmd, shell=True, universal_newlines=True, capture_output=True, text=True)
      if cp.returncode != 0:
        if ('ERROR: [youtube]' in cp.stdout and ('Video unavailable' in cp.stdout or 'This video is unavailable' in cp.stdout or 'Private video' in cp.stdout)) \
                or ('ERROR: [youtube]' in cp.stderr and ('Video unavailable' in cp.stderr or 'This video is unavailable' in cp.stderr or 'Private video' in cp.stderr)):
          error_queue.put(videoid)
          error_vids.add(videoid)
        continue
      result = cp.stdout
      #result = subprocess.check_output(cmd, shell=True, universal_newlines=True)
      auto_lang, manu_lang = get_subtitle_language(result)
      out_queue.put((videoid, auto_lang, manu_lang))
    except:
      traceback.print_exc()
    # sleep
    if wait_sec > 0.01:
      time.sleep(wait_sec)

  os.remove(cookie_file)
  print(proxy, 'done')
  error_queue.put('STOP')

def write_worker(lang, fn_sub, subtitle_exists, in_queue):
  for videoid, auto_lang, manu_lang in iter(in_queue.get, "STOP"):
    subtitle_exists = pd.concat([subtitle_exists, pd.DataFrame([{"videoid": videoid, "auto": lang in auto_lang, "sub": lang in manu_lang}])], ignore_index=True)
    # write current result
    if len(subtitle_exists) % 10 == 0:
      subtitle_exists.to_csv(fn_sub, index=None)

  # write
  subtitle_exists.to_csv(fn_sub, index=None)
  print('write done')

def save_error_worker(error_fn, in_queue):
  with open(str(error_fn), "w") as f:
    for videoid in iter(in_queue.get, "STOP"):
      f.write(videoid+'\n')
      f.flush()
  print('save error done')

def retrieve_subtitle_exists(lang, fn_videoid, proxies, outdir="sub", wait_sec=0.2, fn_checkpoint=None):
  fn_sub = Path(outdir) / lang / f"{Path(fn_videoid).stem}.csv"
  fn_sub.parent.mkdir(parents=True, exist_ok=True)

  # if file exists, load it and restart retrieving.
  if fn_checkpoint is None:
    subtitle_exists = pd.DataFrame({"videoid": [], "auto": [], "sub": []}, dtype=str)
  else:
    subtitle_exists = pd.read_csv(fn_checkpoint)

  vids = set(subtitle_exists["videoid"])
  task_queue = Queue(maxsize=len(proxies))
  done_queue = Queue()
  error_queue = Queue()
  error_fn = Path(f'videoid/error/{lang}wiki-latest-pages-articles-multistream-index.txt')
  if not error_fn.exists():
    error_fn.parent.mkdir(parents=True, exist_ok=True)
    error_fn.touch()
  error_vids = set()
  with open(str(error_fn), "r") as f:
    for line in f.readlines():
      vid = line.strip()
      error_queue.put(vid)
      error_vids.add(vid)

  # Start worker processes
  Process(
    target=write_worker,
    args=(
      lang, fn_sub, subtitle_exists, done_queue
    ),
  ).start()
  for proxy in proxies:
    Process(
      target=retrieve_worker,
      args=(
        proxy, lang, task_queue, done_queue, error_queue, error_vids, wait_sec
      ),
    ).start()
  Process(
    target=save_error_worker,
    args=(
      error_fn, error_queue
    ),
  ).start()
  with open(fn_videoid) as f:
    nvids = f.readlines()
  print(len(vids), len(nvids))
  for videoid in tqdm(nvids):
    videoid = videoid.strip(" ").strip("\n")
    if videoid in vids:
      continue
    task_queue.put(videoid)

  for _ in proxies:
    task_queue.put("STOP")
  while not task_queue.empty() or not done_queue.empty():
    time.sleep(20)
  done_queue.put("STOP")
  return fn_sub

if __name__ == "__main__":
  args = parse_args()

  filename = retrieve_subtitle_exists(args.lang, args.videoidlist, args.proxies, \
    args.outdir, fn_checkpoint=args.checkpoint)
  print(f"save {args.lang.upper()} subtitle info to {filename}.")
