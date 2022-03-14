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

                
    def __call__(self):
        return self.audio_sampling()

if __name__ == '__main__':
    url = '_PaC2nJIhgE'
    sample_aud = AudioSampling(url)
    sample_aud()

    # delete the sampled audio file
    #os.remove(f'{url}.opus')

