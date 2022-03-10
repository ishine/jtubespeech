import torchaudio
from speechbrain.pretrained import EncoderClassifier

# load the voxlingua107 pretrained model from speechbrain
language_id = EncoderClassifier.from_hparams(source="TalTechNLP/voxlingua107-epaca-tdnn", savedir="tmp")
# Download Thai language sample from Omniglot and cvert to suitable form
# signal = language_id.load_audio("https://omniglot.com/soundfiles/udhr/udhr_th.mp3")
signal = language_id.load_audio("../barca_spanish.opus")
prediction =  language_id.classify_batch(signal)
print(prediction)
print()
print(prediction[3])