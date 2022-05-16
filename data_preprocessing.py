import os
import yaml
import tarfile
from tqdm import tqdm
from pathlib import Path
from utils_jtubespeech import RestructureFileDirectoryJtubespeech
from utils_jtubespeech import UtilsJtubespeech


class DataPreprocessingJtubespeech():
    
    def __init__(self, main_data_folder, preprocessed_data_folder, audio_format):
        self.main_data_folder = main_data_folder
        self.preprocessed_data_folder = preprocessed_data_folder
        self.audio_format = audio_format

    def data_preprocessing(self):
        # walk and find all .wav and .vtt file
        for root, dirs, files in tqdm(os.walk(self.main_data_folder)):

            # calling the class object
            preprocess = UtilsJtubespeech(main_data_folder=self.main_data_folder,
                                          preprocessed_data_folder=self.preprocessed_data_folder,
                                          audio_format=self.audio_format)

            # function call to define the preprocessed directory for the processed data (text and audio)
            root_preprocessed = preprocess.get_preprocessed_dirname(root)
            
            # create the preprocessed data directory
            preprocess.create_new_dir(f'./{root_preprocessed}/')

            for file in files:
                # join the root and the filepath to access the textgrid data
                file_access = os.path.join(root, file)
                
                # check for files with .vtt extension
                if file.endswith('.vtt'):
                    data_dict = preprocess.get_vtt_values(file_access)
                    preprocess.write_to_txt_file(f'{root_preprocessed}/{Path(file_access).stem}.trans.txt', data_dict)
                    
                elif file.endswith('.wav'):
                    # get the vtt filename and extension (because same filename for .wav and .vtt)
                    file_access_vtt = file_access.split('.')
                    
                    # extract the required data (in a dictionary) from the .vtt file
                    data_dict = preprocess.get_vtt_values(filepath=f'{file_access_vtt[0]}.vtt')
                    
                    # slice the audio files based on the start and end timing
                    preprocess.slice_audio(file_access, root_preprocessed, data_dict)
        
        print('Done: Preprocessing')

    def make_tarfile(self, output_name, src_dir):
        with tarfile.open(output_name,"w:gz") as tar:
            tar.add(src_dir,arcname=os.path.basename(src_dir))
        
        print('Done: Compressing')

    def __call__(self):
        return self.data_preprocessing()


if __name__ == '__main__':

    # CONFIG IMPORTED FROM .YAML FILE
    with open('./config/config_jtubespeech.yaml') as f:
        config = yaml.safe_load(f)
    
    ## RESTRUCTURING THE JTUBESPEECH DATA FILE DIRECTORY
    file_combine_vtt = RestructureFileDirectoryJtubespeech(root_folder=config['root_folder'], 
                                                            dest_folder=config['dest_folder_name'], 
                                                            file_type=config['file_type_vtt'])

    file_combine_wav = RestructureFileDirectoryJtubespeech(root_folder=config['root_folder'], 
                                                            dest_folder=config['dest_folder_name'],
                                                            file_type=config['file_type_wav'])

    file_combine_vtt()
    file_combine_wav()

    ## DATA PREPROCESSING OF THE JTUBESPEECH DATA TO THE LIBRISPEECH FORMAT
    preprocess = DataPreprocessingJtubespeech(main_data_folder = config['main_data_folder'],
                                              preprocessed_data_folder = config['preprocessed_data_folder'],
                                              audio_format = config['audio_format'])

    preprocess()

    ## MAKE IT INTO A .tar.gz compressed folder
    #preprocess.make_tarfile(f'./{config["preprocessed_data_folder"]}.tar.gz', f'./{config["preprocessed_data_folder"]}')
