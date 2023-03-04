#!/bin/bash
# remove the language2 flag if only scraping one language subtitle

LANGUAGE="ms"
LANGUAGE2="en"
BATCH_CSV_FILE="video_id_with_sub/ms/ms_3/csv_batch/ms_3_batch_11.csv"
OUTPUT_DIR="video"

python3 download_video.py \
    --language ${LANGUAGE} \
    --sublist ${BATCH_CSV_FILE} \
    --outdir ${OUTPUT_DIR}