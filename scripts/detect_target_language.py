import torchaudio
import os
from speechbrain.pretrained import EncoderClassifier
from util import load_mapping
import cld3

class DetectTargetLanguage():
    
    def __init__(self, url_id, language_code, threshold):
        self.url_id = url_id
        self.language_code = language_code
        self.threshold = threshold

    def get_language_prediction(self):
        # load the voxlingua107 pretrained model from speechbrain
        language_id = EncoderClassifier.from_hparams(source="TalTechNLP/voxlingua107-epaca-tdnn", savedir="tmp")

        signal = language_id.load_audio(f'{self.url_id}.opus')
        prediction =  language_id.classify_batch(signal)

        return prediction

    # language identification for audio
    def check_target_language_audio(self):
        prediction = self.get_language_prediction()

        # load the key value pair of the language id and the number tagged to it from the dictionary
        mapping = load_mapping()

        target_lang_idx = mapping.get(self.language_code)

        print(f'Audio target language probability: {prediction[0][0].numpy()[target_lang_idx]}')

        if prediction[0][0].numpy()[target_lang_idx] > self.threshold:
            print("Audio: That's the target language")
            return True
        else:
            print("Audio: That's not the target language")
            return False

    def get_video_title_and_rename_audio(self):
        # call this code only at the base directory - i.e /jtubespeech
        # make sure there is no .opus file in the base directory
        # rename the audio file to the filename same as the one in the csv file
        for file in os.listdir('.'):
            if file.endswith('.opus'):
                os.rename(file, f'{self.url_id}.opus')
        
                youtube_vid_title = file.replace(f'-{self.url_id}.opus', '')
                return youtube_vid_title
    
    # language identification for video title
    def check_target_language_video_title(self):
        youtube_vid_title = self.get_video_title_and_rename_audio()
        language_pred = cld3.get_language(youtube_vid_title)
        if language_pred.language == self.language_code:
            print("Youtube Title: That's the target language")
            return True
        else:
            print("Youtube Title: That's not the target language")
            return False
    
    # def __call__(self):
    #     return self.check_target_language_video_title()

if __name__ == '__main__':
    # debugging code to debug this file individually with example audio
    URL_ID = "_PaC2nJIhgE"
    LANGUAGE_CODE = 'id'
    THRESHOLD = 0.8
    
    lang_prediction = DetectTargetLanguage(url_id=URL_ID,
                                           language_code=LANGUAGE_CODE,
                                           threshold=THRESHOLD)
    
    # need to run this first to rename the filename

    # uncomment this if NOT checking the file title
    #youtube_vid_title = lang_prediction.get_video_title_and_rename_audio() 

    # uncomment this if checking the file title
    check_text = lang_prediction.check_target_language_video_title()
    print(f'Youtube Title: {check_text}')

    prediction = lang_prediction.get_language_prediction()
    print(prediction)
    print()

    check_audio = lang_prediction.check_target_language_audio()
    print(f'Audio: {check_audio}')
    

    # after prediction, the sampled audio file is not needed anymore
    os.remove(f'{URL_ID}.opus')