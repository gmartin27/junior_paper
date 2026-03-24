import os
from nltk.sentiment import SentimentIntensityAnalyzer
import argparse
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sia = SentimentIntensityAnalyzer()
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--out")
    parser.add_argument("--plot")
    parser.add_argument("--comp_list")
    args = parser.parse_args()

    compounds = []
    texts = {}
    for file in os.listdir(args.corpus):
        if file.endswith(".txt"):
            with open(os.path.join(args.corpus, file), "r", encoding="utf-8") as f:
                texts[file] = f.read()

    results = {}
    most_neg = {"doc": None, "comp": float('inf')}
    most_pos = {"doc": None, "comp": -float('inf')}
    pos_count = 0
    neg_count = 0
    neu_count = 0

    total_compound = 0
    for filename, text in texts.items():
        scores = sia.polarity_scores(text)
        results[filename] = scores
        comp = scores["compound"]
        compounds.append(comp)
        total_compound += comp

        if comp > most_pos["comp"]:
            most_pos = {"doc": filename, "comp": comp}
        if comp < most_neg["comp"]:
            most_neg = {"doc": filename, "comp": comp}

        if comp > 0.0:
            pos_count += 1
        elif comp < 0.0:
            neg_count += 1
        else:
            neu_count += 1
    
    results = sorted(results.items(), key = lambda item: item[1]["compound"], reverse=True)

    if args.plot:
        plt.figure(figsize=(10,6))
        n, bins, patches = plt.hist(compounds, bins=20, range=(-1,1), color='blue', edgecolor='black', alpha=0.7)
        plt.title(f'Distribution of Sentiment Compound Scores for {args.corpus}', fontsize=14)
        plt.xlabel('Sentiment Score', fontsize=12)
        plt.ylabel('Frequency (Number of Posts)', fontsize=12)
        plt.xlim(-1,1)
        plt.axvline(0, color='red', linestyle='dashed',linewidth=1)
        plt.savefig(args.plot)

    if args.comp_list:
        with open(args.comp_list, "a", encoding="utf-8") as f:
            for compound in compounds:
                f.write(f'{compound}\n')

    if args.out:
        with open(args.out, "a", encoding="utf-8") as f:
            avg_sent = total_compound/len(texts)
            print(f"Average Sentiment of Corpus Texts: {avg_sent}")
            f.write(f"Average Sentiment of Corpus Texts: {avg_sent}\n")
            print(f"Most negative: {most_neg}")
            print(f"Most positive: {most_pos}")
            print(f"Positive count: {pos_count}")
            print(f"Neutral count: {neu_count}")
            print(f"Negative count: {neg_count}")

            for filename, scores in results:
                f.write(f"{filename}: {scores}")
                f.write("\n")
    else:
        print(f"Average Sentiment of Corpus Texts: {total_compound/len(texts)}")
        print(f"Most negative: {most_neg}")
        print(f"Most positive: {most_pos}")
        print(f"Positive count: {pos_count}")
        print(f"Neutral count: {neu_count}")
        print(f"Negative count: {neg_count}")

