#!/bin/bash

LANGUAGE="ms"
INPUT_CSV_FILEPATH="video_id_with_sub/ms/ms_3/ms_3.csv"
ENTRIES_PER_CSV_BATCH=10

python3 batching.py \
    --language ${LANGUAGE} \
    --raw_csv ${INPUT_CSV_FILEPATH} \
    --entries ${ENTRIES_PER_CSV_BATCH}