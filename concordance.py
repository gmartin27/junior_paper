import nltk
from nltk.corpus import PlaintextCorpusReader as corp_reader
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--words", nargs='+', required=True)
    parser.add_argument("--lines", default=20)
    args = parser.parse_args()

    wordlists = corp_reader(args.corpus, '.*', encoding='latin-1')

    text = nltk.Text(wordlists.words())

    for word in args.words:
        print(f"Context for {word}: ")
        text.concordance(word, width=80, lines=int(args.lines))
