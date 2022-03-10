# a python module that removes the data where the column 'sub' == False obtained from retrieve_subtitle_exists.py 
# since it will not be used in the download_video.py
# it will also split the csv into batches for easier parallel run when downloading the videos later

import pandas as pd
import os

class DataframePruningAndBatching():
    def __init__(self, lang_code, source_csv_path, dest_dir, entries_per_csv):
        self.lang_code = lang_code
        self.source_csv_path = source_csv_path
        self.dest_dir = dest_dir
        self.entries_per_csv = entries_per_csv

    def remove_unwanted_row(self):
        # reads the csv generated from retrieve_subtitle_exists.py
        df_ = pd.read_csv(self.source_csv_path)

        # creates new dataframe with only column 'sub' == True
        df = df_[df_['sub'] == True]

        # reoder the dataframe by the 'auto' column
        df = df.sort_values(by=['auto'], ascending=True)

        # create new subdirectory in the 'sub' main folder
        self.create_new_dir()

        # split the csv files into batches of csv files
        self.split_into_batches(df)

    # split the csv files into batches of csv files
    def split_into_batches(self, df):
        for batch in range((len(df)-1) // self.entries_per_csv + 1):
            if batch != (len(df)-1) // self.entries_per_csv + 1:
                df_batch = df.iloc[batch*self.entries_per_csv: (batch+1)*self.entries_per_csv]
            else:
                df_batch = df.iloc[batch*self.entries_per_csv:]
            df_batch.to_csv(f'{self.dest_dir}{self.lang_code}_{batch+1}.csv', index=False)
            print(f'Batch {batch+1}: Done')
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
    LANG_CODE = 'id'
    SOURCE_CSV = './sub/id/test.csv'
    DEST_DIR = './sub/id/csv_batch/'
    ENTRIES_PER_CSV = 50

    df_pruning_batching = DataframePruningAndBatching(lang_code=LANG_CODE, 
                                             source_csv_path=SOURCE_CSV, 
                                             dest_dir=DEST_DIR, 
                                             entries_per_csv=ENTRIES_PER_CSV)
    df_pruning_batching()