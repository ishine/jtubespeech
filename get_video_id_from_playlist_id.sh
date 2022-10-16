#!/bin/bash

CHANNEL_ID_TEXT_FILEPATH="playlist_id/ms/ms_1.txt"
VIDEO_ID_TEXT_FILEPATH="video_id/ms/ms_1.txt"
ID_TYPE="playlist"
SLEEP=2

python3 get_video_id.py \
    --channel_id "${CHANNEL_ID_TEXT_FILEPATH}" \
    --video_id "${VIDEO_ID_TEXT_FILEPATH}" \
    --id_type "${ID_TYPE}" \
    --sleep "${SLEEP}"