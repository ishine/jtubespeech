#!/bin/bash
ROOT_FOLDER="./datasets/jtubespeech/jtubespeech_data_small/id"
DEST_FOLDER_NAME="annotated_data"
FILE_TYPE_VTT="vtt"
FILE_TYPE_WAV="wav16k"
MAIN_DATA_FOLDER="datasets/jtubespeech/jtubespeech_data_small/id/annotated_data"
PREPROCESSED_DATA_FOLDER="datasets/jtubespeech/jtubespeech_data_small/id/annotated_data_preprocessed_wav"
AUDIO_FORMAT="wav"

python3 ../data_preprocessing.py \
    --root_folder ${ROOT_FOLDER} \
    --dest_folder_name ${DEST_FOLDER_NAME} \
    --file_type_vtt ${FILE_TYPE_VTT} \
    --file_type_wav ${FILE_TYPE_WAV} \
    --main_data_folder ${MAIN_DATA_FOLDER} \
    --preprocessed_data_folder ${PREPROCESSED_DATA_FOLDER} \
    --audio_format ${AUDIO_FORMAT} 