#!/bin/bash

LANGUAGE="ms"
INPUT_CSV_FILEPATH="video_id_with_sub/ms/ms_1/ms_1.csv"
ENTRIES_PER_CSV_BATCH=15

python3 batching.py \
    --language ${LANGUAGE} \
    --raw_csv ${INPUT_CSV_FILEPATH} \
    --entries ${ENTRIES_PER_CSV_BATCH}