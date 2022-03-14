# samples the audio taken from the youtube link for prediction of language later to avoid large download of the file
import numpy as np
import subprocess
import os

class AudioSampling():
    def __init__(self, url_id):
        self.url_id = url_id

    def audio_sampling(self):
        cp = subprocess.run(f'youtube-dl -f 251 https://www.youtube.com/watch?v={self.url_id} -x --external-downloader ffmpeg --external-downloader-args "-ss 00:00:50.00 -t 00:00:20.00"', shell=True, universal_newlines=True)

        if cp.returncode != 0:
            print(f"Failed to download the video: url = {self.url_id}")

        # call this code only at the base directory - i.e /jtubespeech
        # make sure there is no .opus file in the base directory

        # rename the audio file to the filename same as the one in the csv file
        for file in os.listdir('.'):
            if file.endswith('.opus'):
                os.rename(file, f'{self.url_id}.opus')

    def __call__(self):
        return self.audio_sampling()


if __name__ == '__main__':
    url = 'QbtV4QRi2os'
    #TARGET_LANG = 'es'
    sample_aud = AudioSampling(url)
    sample_aud()

    # delete the sampled audio file
    #os.remove(f'{url}.opus')

