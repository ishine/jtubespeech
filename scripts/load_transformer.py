import torchaudio
from speechbrain.pretrained import EncoderClassifier

class AudioLanguagePrediction():
    
    def __init__(self, filepath):
        self.filepath = filepath

    def get_prediction(self):
        # load the voxlingua107 pretrained model from speechbrain
        language_id = EncoderClassifier.from_hparams(source="TalTechNLP/voxlingua107-epaca-tdnn", savedir="tmp")

        signal = language_id.load_audio(self.filepath)
        prediction =  language_id.classify_batch(signal)

        print(prediction)
        print()
        print(prediction[3])

        #return prediction
    
    def __call__(self):
        return self.get_prediction()

if __name__ == '__main__':
    FILEPATH = "../barca_spanish.opus"
    lang_prediction = AudioLanguagePrediction(filepath=FILEPATH)
    lang_prediction()