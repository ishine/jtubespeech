# a python module that removes the data where the column 'sub' == False obtained from retrieve_subtitle_exists.py 
# since it will not be used in the download_video.py
# also, it sorts the df based on the column 'auto'

import pandas as pd
import os

class DataframePruning():
    def __init__(self, source_csv_path, dest_dir, dest_csv_filename):
        self.source_csv_path = source_csv_path
        self.dest_dir = dest_dir
        self.dest_csv_filename = dest_csv_filename

    def remove_unwanted_row(self):
        # reads the csv generated from retrieve_subtitle_exists.py
        df_ = pd.read_csv(self.source_csv_path)

        # creates new dataframe with only column 'sub' == True
        df = df_[df_['sub'] == True]

        # reoder the dataframe by the 'auto' column
        df = df.sort_values(by=['auto'], ascending=True)

        # create new subdirectory in the 'sub' main folder
        self.create_new_dir()

        # export the edited dataframe into another directory
        # add the batch number later...
        df.to_csv(f'{self.dest_dir}{self.dest_csv_filename}', index=False)
        print('Done!')

    # create new directory and ignore already created ones
    def create_new_dir(self):
        try:
            os.mkdir(self.dest_dir)
        except OSError as error:
            pass # directory already exists!

    def __call__(self):
        return self.remove_unwanted_row()

if __name__ == '__main__':
    SOURCE_CSV = './sub/id/test.csv'
    DEST_DIR = './sub/id/csv_batch/'
    DEST_CSV_FILENAME = 'test_edited.csv'

    df_pruning = DataframePruning(source_csv_path=SOURCE_CSV, 
                                  dest_dir=DEST_DIR, 
                                  dest_csv_filename=DEST_CSV_FILENAME)
    df_pruning()