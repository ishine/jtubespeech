import time
import requests
import argparse
import re
import os
import sys
import subprocess
from pathlib import Path
from util import make_video_url, get_subtitle_language
import pandas as pd
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(
        description="Retrieving whether subtitles exists or not.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--language",           type=str, help="the targeted language code (ISO 639-1) (eg. ja, en, ...)")
    parser.add_argument("--language2",          type=str, default=None, help="second lanugage for translation - the targeted language code (ISO 639-1) (eg. ja, en, ...)")
    parser.add_argument("--video_id_list",      type=str, help="filename of video ID list")
    parser.add_argument("--main_outdir",        type=str, default="video_id_with_sub", help="main output directory")
    parser.add_argument("--sub_outdir",         type=str, help="sub output directory")
    parser.add_argument("--sub_sub_outdir",     type=str, help="sub sub output directory")
    parser.add_argument("--csv_filepath",       type=str, help="filepath of the final csv file")
    parser.add_argument("--checkpoint",         type=str, default=None, help="filename of list checkpoint (for restart retrieving)")
    
    return parser.parse_args(sys.argv[1:])

def create_new_dir(directory: str) -> None:
    '''
        creates new directory and ignore already created ones
        directory: the directory path that is being created
    '''
    try:
        os.mkdir(directory)
    except OSError as error:
        pass # directory already exists!

def retrieve_subtitle_exists(lang, fn_videoid, main_outdir, sub_outdir, sub_sub_outdir, csv_filepath, lang2="", wait_sec=0.2, fn_checkpoint=None):

    # create new directory and the subsequent sub directories to store the final csv file
    create_new_dir(main_outdir)
    create_new_dir(sub_outdir)
    create_new_dir(sub_sub_outdir)

    #fn_sub = Path(outdir) / lang / f"{Path(fn_videoid).stem}.csv"
    #fn_sub.parent.mkdir(parents=True, exist_ok=True)
    
    # final csv output filepath
    fn_sub = csv_filepath

    # if file exists, load it and restart retrieving.
    if fn_checkpoint is None:
        subtitle_exists = pd.DataFrame(
            {"videoid": [], "auto": [], "sub": []}, dtype=str)
    else:
        subtitle_exists = pd.read_csv(fn_checkpoint)

    # load video ID list
    n_video = 0
    for videoid in tqdm(open(fn_videoid).readlines()):
        videoid = videoid.strip(" ").strip("\n")
        if videoid in set(subtitle_exists["videoid"]):
            continue

        # send query to YouTube
        url = make_video_url(videoid)
        try:
            result = subprocess.check_output(f"youtube-dl --list-subs --sub-lang {lang} --skip-download {url}",
                                             shell=True, universal_newlines=True)
            auto_lang, manu_lang = get_subtitle_language(result)
        #   subtitle_exists = subtitle_exists.append( \
        #     {"videoid": videoid, "auto": lang in auto_lang, "sub": lang in manu_lang},
        #     ignore_index=True)

            # if the second language is not stated
            if not lang2:
                subtitle_exists = pd.concat([subtitle_exists, pd.DataFrame.from_records(
                    [{"videoid": videoid, "auto": lang in auto_lang, "sub": lang in manu_lang}])])
            # if second language is stated - translation tasks
            else:
                subtitle_exists = pd.concat([subtitle_exists, pd.DataFrame.from_records(
                    [{"videoid": videoid, "auto": lang in auto_lang, "sub": lang in manu_lang, "auto2": lang2 in auto_lang, "sub2": lang2 in manu_lang}])])
            n_video += 1
            
        except:
            print('error')
            continue

        # write current result
        if n_video % 100 == 0:
            subtitle_exists.to_csv(fn_sub, index=None)

        # sleep
        if wait_sec > 0.01:
            time.sleep(wait_sec)

    # write
    subtitle_exists.to_csv(fn_sub, index=None)
    return fn_sub


if __name__ == "__main__":
    args = parse_args()

    filename = retrieve_subtitle_exists(lang=args.language, 
                                        lang2=args.language2,
                                        fn_videoid=args.video_id_list,
                                        main_outdir=args.main_outdir, 
                                        sub_outdir=args.sub_outdir, 
                                        sub_sub_outdir=args.sub_sub_outdir, 
                                        csv_filepath=args.csv_filepath)

    print(f"save {args.language.upper()} subtitle info to {filename}.")
