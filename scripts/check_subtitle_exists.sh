#!/bin/bash

LANGUAGE="id"
VIDEO_ID_LIST="video_id/id/id_small_demo.txt"
MAIN_DIR="video_id_with_sub"
SUB_SUB_DIR="id_small_demo"

python3 ../check_subtitle_exists.py \
    --language ${LANGUAGE} \
    --video_id_list "../${VIDEO_ID_LIST}" \
    --main_outdir "../${MAIN_DIR}/" \
    --sub_outdir "../${MAIN_DIR}/${LANGUAGE}/" \
    --sub_sub_outdir "../${MAIN_DIR}/${LANGUAGE}/${SUB_SUB_DIR}/" \
    --csv_filepath "../${MAIN_DIR}/${LANGUAGE}/${SUB_SUB_DIR}/${SUB_SUB_DIR}.csv"
    