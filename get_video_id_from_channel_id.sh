#!/bin/bash

CHANNEL_ID_TEXT_FILEPATH="channel_id/id/id_small_demo2.txt"
VIDEO_ID_TEXT_FILEPATH="video_id/id/id_small_demo2.txt"
ID_TYPE="channel"

python3 get_video_id.py \
    --channel_id "${CHANNEL_ID_TEXT_FILEPATH}" \
    --video_id "${VIDEO_ID_TEXT_FILEPATH}" \
    --id_type "${ID_TYPE}"