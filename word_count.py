import nltk
from nltk.corpus.reader import PlaintextCorpusReader as corp_reader
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    args = parser.parse_args()

    corpus = corp_reader(args.corpus, '.*', encoding="latin-1")

    post_lengths = [len(corpus.words(file)) for file in corpus.fileids()]

    max_len = max(post_lengths)
    min_len = min(post_lengths)
    avg = sum(post_lengths) / len(post_lengths)
    median = np.median(post_lengths)

    print(f"Total Posts: {len(post_lengths)}\nLongest: {max_len}\nShortest: {min_len}\nAverage: {avg}\nMedian: {median}")
