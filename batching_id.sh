#!/bin/bash

LANGUAGE="id"
INPUT_CSV_FILEPATH="video_id_with_sub/id/id_small_demo/id_small_demo.csv"
ENTRIES_PER_CSV_BATCH=13

python3 batching.py \
    --language ${LANGUAGE} \
    --raw_csv ${INPUT_CSV_FILEPATH} \
    --entries ${ENTRIES_PER_CSV_BATCH}