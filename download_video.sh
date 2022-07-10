#!/bin/bash

LANGUAGE="id"
BATCH_CSV_FILE="video_id_with_sub/id/id_small_demo/csv_batch/id_small_demo_batch_4.csv"
OUTPUT_DIR="video"

python3 download_video.py \
    --language ${LANGUAGE} \
    --sublist ${BATCH_CSV_FILE} \
    --outdir ${OUTPUT_DIR}