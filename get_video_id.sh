#!/bin/bash

CHANNEL_ID_TEXT_FILEPATH="channel_id/id/id_small_demo.txt"
VIDEO_ID_TEXT_FILEPATH="video_id/id/id_small_demo.txt"

python3 get_video_id.py \
    --channel_id "${CHANNEL_ID_TEXT_FILEPATH}" \
    --video_id "${VIDEO_ID_TEXT_FILEPATH}"