import torchaudio
import os
from speechbrain.pretrained import EncoderClassifier
from util import load_mapping

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

    def check_target_language(self):
        prediction = self.get_language_prediction()

        # load the key value pair of the language id and the number tagged to it from the dictionary
        mapping = load_mapping()

        target_lang_idx = mapping.get(self.language_code)

        print(f'Target language probability: {prediction[0][0].numpy()[target_lang_idx]}')

        if prediction[0][0].numpy()[target_lang_idx] > 0.8:
            print("That's the target language")
            return True
        else:
            print("That's not the target language")
            return False
    
    def __call__(self):
        return self.check_target_language()

if __name__ == '__main__':
    # debugging code to debug this file individually with example audio
    URL_ID = "QbtV4QRi2os"
    LANGUAGE_CODE = 'es'
    THRESHOLD = 0.8
    
    lang_prediction = DetectTargetLanguage(url_id=URL_ID,
                                           language_code=LANGUAGE_CODE,
                                           threshold=THRESHOLD)
    prediction = lang_prediction.get_language_prediction()
    print(prediction)
    print()
    lang_prediction()

    # after prediction, the sampled audio file is not needed anymore
    os.remove(f'{URL_ID}.opus')