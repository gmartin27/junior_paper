from nltk.corpus import PlaintextCorpusReader as corp_reader
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    tok = RegexpTokenizer(r"[A-Za-z]+(?:'[A-Za-z]+)?")

    corpus = corp_reader(args.corpus, r".*\.txt", word_tokenizer=tok)
    tokens = corpus.words()
    types = set(tokens)

    tok_freq = len(tokens)
    typ_freq = len(types)
    
    freq_dist = FreqDist(tokens)

    lines = [
        f"Corpus file: {args.corpus}",
        f"Number of tokens/words: {tok_freq}",
        f"Number of types/unique words: {typ_freq}",
        f"Top 20 words: {freq_dist.most_common(20)}"
    ]

    for line in lines:
        print(line)

    if args.out:
        with open(args.out, "a", encoding="utf-8") as f:
            f.write("\n")
            for line in lines:
                f.write(line + "\n")
