import time
import argparse
import sys
import subprocess
import shutil

import pydub
from pathlib import Path
from util import make_video_url, make_basename, vtt2txt, autovtt2txt
import pandas as pd
from tqdm import tqdm
import os

# self defined modules
from detect_target_language import DetectTargetLanguage
from sample_audio import AudioSampling


def parse_args():
    parser = argparse.ArgumentParser(
        description="Downloading videos with subtitle.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("lang",         type=str,
                        help="language code (ja, en, ...)")
    parser.add_argument("sublist",      type=str,
                        help="filename of list of video IDs with subtitles")
    parser.add_argument("--threshold",     type=float,
                        default=0.7, help="probability threshold to determine if it is target language")
    parser.add_argument("--check_audio_and_title",  action='store_true',
                        default=False, help="check if video's title and audio needs to be checked")
    parser.add_argument("--outdir",     type=str,
                        default="video", help="dirname to save videos")
    parser.add_argument("--keeporg",    action='store_true',
                        default=False, help="keep original audio file.")
    return parser.parse_args(sys.argv[1:])


def download_video(lang, fn_sub, outdir="video", wait_sec=10, keep_org=False):
    """
    Tips:
      If you want to download automatic subtitles instead of manual subtitles, please change as follows.
        1. replace "sub[sub["sub"]==True]" of for-loop with "sub[sub["auto"]==True]"
        2. replace "--write-sub" option of youtube-dl with "--write-auto-sub"
        3. replace vtt2txt() with autovtt2txt()
        4 (optional). change fn["vtt"] (path to save subtitle) to another. 
    """

    # parse args to take in the language code
    args = parse_args()

    sub = pd.read_csv(fn_sub)

    # initialise number of successful scrape
    success_count = 0

    for videoid in tqdm(sub[sub["sub"] == True]["videoid"]):  # manual subtitle only
        
        ## ADDITIONAL CODES TO CHECK IF AUDIO AND TEXT ARE TARGET LANGUAGE OR NOT
        if args.check_audio_and_title:

            # SAMPLE THE AUDIO
            sample_aud = AudioSampling(url_id=videoid)
            sample_aud()

            # CHECK IF THE AUDIO IS THE TARGET TRANSCRIPT LANGUAGE
            predict_target_lang = DetectTargetLanguage(url_id=videoid, 
                                                    language_code=args.lang,
                                                    threshold=args.threshold)
            try:
                # this checks the youtube video title if it is the same as the target language
                check_text = predict_target_lang.check_target_language_video_title()
                # this checks if the audio scraped is the same as the target language
                check_audio = predict_target_lang.check_target_language_audio()
            except:
                continue # error in scraping info

            # remove the .opus audio file from root folder
            for item in os.listdir('.'):
                if item.endswith('.opus'):
                    os.remove(item)

            # IF THE SAMPLED AUDIO FILE'S PREDICTED LANGUAGE IS THE TARGET LANGUAGE, CONTINUE TO DOWNLOAD THE AUDIO
            # ELSE, DO NOT DOWNLOAD THE AUDIO AND GO TO THE NEXT ITERATION
            if not (check_text and check_audio):
                continue

        fn = {}
        for k in ["wav", "wav16k", "vtt", "txt"]:
            fn[k] = Path(outdir) / lang / k / \
                (make_basename(videoid) + "." + k[:3])
            fn[k].parent.mkdir(parents=True, exist_ok=True)

        if not fn["wav16k"].exists() or not fn["txt"].exists():
            print(videoid)

            # download
            url = make_video_url(videoid)
            base = fn["wav"].parent.joinpath(fn["wav"].stem)
            cp = subprocess.run(
                f"youtube-dl --sub-lang {lang} --extract-audio --audio-format wav --write-sub {url} -o {base}.\%\(ext\)s", shell=True, universal_newlines=True)
            if cp.returncode != 0:
                print(f"Failed to download the video: url = {url}")
                continue
            try:
                shutil.move(f"{base}.{lang}.vtt", fn["vtt"])
            except Exception as e:
                print(
                    f"Failed to rename subtitle file. The download may have failed: url = {url}, filename = {base}.{lang}.vtt, error = {e}")
                continue

            # vtt -> txt (reformatting)
            try:
                txt = vtt2txt(open(fn["vtt"], "r").readlines())
                with open(fn["txt"], "w") as f:
                    f.writelines(
                        [f"{t[0]:1.3f}\t{t[1]:1.3f}\t\"{t[2]}\"\n" for t in txt])
            except Exception as e:
                print(
                    f"Falied to convert subtitle file to txt file: url = {url}, filename = {fn['vtt']}, error = {e}")
                continue

            # wav -> wav16k (resampling to 16kHz, 1ch)
            try:
                wav = pydub.AudioSegment.from_file(fn["wav"], format="wav")
                wav = pydub.effects.normalize(
                    wav, 5.0).set_frame_rate(16000).set_channels(1)
                wav.export(fn["wav16k"], format="wav", bitrate="16k")
            except Exception as e:
                print(
                    f"Failed to normalize or resample downloaded audio: url = {url}, filename = {fn['wav']}, error = {e}")
                continue

            # remove original wav
            if not keep_org:
                fn["wav"].unlink()

            # wait
            if wait_sec > 0.01:
                time.sleep(wait_sec)
        
        success_count += 1

    print('\n---------------------------------\n')
    print(f'Number of successful scrape in this batch: {success_count}/{len(sub[sub["sub"] == True]["videoid"])}')
    print('\n---------------------------------\n')
    return Path(outdir) / lang


if __name__ == "__main__":
    args = parse_args()

    dirname = download_video(args.lang, args.sublist, args.outdir)
    print(f"save {args.lang.upper()} videos to {dirname}.")
