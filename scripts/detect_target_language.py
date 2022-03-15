import os

# transformers - audio
import torchaudio
from speechbrain.pretrained import EncoderClassifier
from util import load_audio_language_mapping, load_text_language_mapping

# transformers - text
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class DetectTargetLanguage():
    
    def __init__(self, url_id, language_code, threshold):
        self.url_id = url_id
        self.language_code = language_code
        self.threshold = threshold

    # get the predicted language and also the probability score from the audio
    def get_language_prediction_audio(self):
        # load the voxlingua107 pretrained model from speechbrain
        language_id = EncoderClassifier.from_hparams(source="TalTechNLP/voxlingua107-epaca-tdnn", savedir="tmp")

        signal = language_id.load_audio(f'{self.url_id}.opus')
        prediction =  language_id.classify_batch(signal)

        return prediction

    # language identification for audio
    def check_target_language_audio(self):
        prediction = self.get_language_prediction_audio()

        # load the key value pair of the language id and the number tagged to it from the dictionary
        mapping = load_audio_language_mapping()

        target_lang_idx = mapping.get(self.language_code)

        print(f'Audio target language probability: {prediction[0][0].numpy()[target_lang_idx]}')

        if prediction[0][0].numpy()[target_lang_idx] > self.threshold:
            print("Audio: That's the target language")
            return True
        else:
            print("Audio: That's not the target language")
            return False

    # rename the scraped audio title to the id which is the same as the videoid in the csv file
    def get_video_title_and_rename_audio(self):
        # call this code only at the base directory - i.e /jtubespeech
        # make sure there is no .opus file in the base directory
        # rename the audio file to the filename same as the one in the csv file
        for file in os.listdir('.'):
            if file.endswith('.opus'):
                os.rename(file, f'{self.url_id}.opus')
        
                youtube_vid_title = file.replace(f'-{self.url_id}.opus', '')
                return youtube_vid_title
    
    # get the predicted language and also the probability score from the video title
    def get_language_prediction_video_title(self):
        # load the pretrained model and the tokenizer
        model = AutoModelForSequenceClassification.from_pretrained("ivanlau/language-detection-fine-tuned-on-xlm-roberta-base")
        tokenizer = AutoTokenizer.from_pretrained("ivanlau/language-detection-fine-tuned-on-xlm-roberta-base")

        # get the video title and rename the audio file to its youtube videoid
        youtube_vid_title = self.get_video_title_and_rename_audio()

        # simple nlp/regex to clean up the text title
        youtube_vid_title = re.sub(r'[^a-zA-Z ]', ' ', youtube_vid_title).lower()
        youtube_vid_title = ' '.join(youtube_vid_title.split())
        print()
        print()
        print(youtube_vid_title)
        print()
        print()
        
        # get the encoding, outputs and logits
        # refer to: https://discuss.huggingface.co/t/decoding-the-predicted-output-array-in-distilbertbase-uncased-model-for-ner/10673
        encoding = tokenizer(youtube_vid_title, return_tensors = 'pt')
        outputs = model(**encoding)
        logits = outputs.logits

        # do the prediction
        predicted_label_classes = logits.argmax(-1)

        # return the predicted language class id
        return predicted_label_classes[0].numpy().tolist()

    # language identification for video title
    def check_target_language_video_title(self):
        # get the predicted language class id
        pred_lang_class_id = self.get_language_prediction_video_title()

        # load the key value pair of the language id and the number tagged to it from the dictionary
        mapping = load_text_language_mapping()
        # get the target language code from the mapping
        target_lang_id = mapping.get(pred_lang_class_id)

        # check if the predicted language id is the same as the target language id
        if target_lang_id == self.language_code:
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

    prediction = lang_prediction.get_language_prediction_audio()
    print(prediction)
    print()

    check_audio = lang_prediction.check_target_language_audio()
    print(f'Audio: {check_audio}')
    

    # after prediction, the sampled audio file is not needed anymore
    os.remove(f'{URL_ID}.opus')