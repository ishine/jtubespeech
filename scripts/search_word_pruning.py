from transformers import AutoTokenizer, AutoModelForSequenceClassification
import argparse
import sys
import os
from util import load_text_language_mapping

def parse_args():
    parser = argparse.ArgumentParser(
        description="Making search words from Wikipedia",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("lang",     type=str,
                        help="language code (ja, en, ...)")
    parser.add_argument("--outdir", type=str, default="word",
                        help="dirname to save words")
    return parser.parse_args(sys.argv[1:])

class SearchWordPruning():
    def __init__(self, file_dir, filtered_file_dir):
        self.file_dir = file_dir
        self.filtered_file_dir = filtered_file_dir

    def prune(self):
        # load pretrained transformer model
        tokenizer = AutoTokenizer.from_pretrained("ivanlau/language-detection-fine-tuned-on-xlm-roberta-base")
        model = AutoModelForSequenceClassification.from_pretrained("ivanlau/language-detection-fine-tuned-on-xlm-roberta-base")

        # get the video text mapping
        text_mapping = load_text_language_mapping()

        # get args
        args = parse_args()

        # initialise count to track the number of lines in the .txt file
        count = 0
        with open(f'{self.file_dir}') as f:
            for line in f.readlines():
                count += 1

                encoding = tokenizer(line.strip(), return_tensors = 'pt')
                outputs = model(**encoding)
                logits = outputs.logits
                predicted_label_classes = logits.argmax(-1)

                target_lang_id = text_mapping.get(predicted_label_classes[0].numpy().tolist())

                if target_lang_id == args.lang:
                    print(f"Line {count}: Youtube Title: That's the target language")
                    with open(f'{self.filtered_file_dir}', 'a+') as fp:
                        fp.write(f'{line.strip()}\n')

                else:
                    print(f"Line {count}: Youtube Title: That's not the target language")

    def __call__(self):
        return self.prune()

if __name__ == '__main__':
    # TRY MAKING IT INTO ARGPARSE WITH DEFAULT
    FILE_DIR = './word/word/id/test.txt'
    FILTERED_FILEDIR = './word/word/id/search_words_filtered.txt'

    pruning_text = SearchWordPruning(FILE_DIR, FILTERED_FILEDIR)
    pruning_text()