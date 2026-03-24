import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
import string
import os
import argparse
from pathlib import Path

def list_text(input_dir):
    text = []

    inp = Path(input_dir)

    for file in inp.rglob("*.txt"):
        post_text = file.read_text(encoding="utf-8")
        posts = [p.strip() for p in post_text.split("\n\n") if p.strip()]
        text.extend(posts)
    
    return(text)

def main(inp, corpus_dir):
    tokenized = []
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r"[A-Za-z]+(?:'[A-Za-z]+)?")
    
    texts = list_text(inp)

    for text in texts:
        words = tokenizer.tokenize(text)
        
        normal = []
        for word in words:
            #if word not in stop_words and word.strip():
            normal.append(word)
        normal_text = " ".join(normal)
        tokenized.append(normal_text)

    if not os.path.exists(str(corpus_dir)):
        os.makedirs(corpus_dir)

    for i, text in enumerate(tokenized):
        with open(os.path.join(corpus_dir, f"doc{i+1}.txt"), "w", encoding="utf-8") as file:
            file.write(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--corpus", required=True)
    args = parser.parse_args()

    main(args.input, args.corpus)
