from scipy.stats import mannwhitneyu
import argparse
import numpy as np

def read_scores(file):
    with open(file, 'r') as f:
        scores = [float(line.strip()) for line in f if line.strip()]

    return scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--A", required=True)
    parser.add_argument("--B", required=True)
    args = parser.parse_args()

    a = read_scores(args.A)
    b = read_scores(args.B)

    stat, p_val = mannwhitneyu(a, b)

    med_a = np.median(a)
    med_b = np.median(b)

    print(f"Median of Dataset A: {med_a}")
    print(f"Median of Dataset B: {med_b}")
    print(f'p-value: {p_val}')
    if p_val < 0.05:
        print("The difference in sentiment distributions is statistically significant.")
