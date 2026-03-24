# Analyzing Possible Gender Bias in Online English-language United States Soccer Discourse
## Junior Paper - Additional Materials

## clean.py
This is the current script used to clean raw data. It takes in a .csv file (`--inp`) and outputs a .txt file (`--out`).

The cleaning process involves:

Removing
- Twitter picture links
- URLs
- the Big Soccer reply pattern
    - USER said: [ORIGINAL\_POSTER'S\_CONTENT] Click to expand...
- "[NUMBER] is not a valid tweet id"
- @s
- #s
- non-ASCII characters
- non-alphanumeric characters (except ')
- non-English entries

and standardizing spacing and case (all lower case).

## concordance.py
This script takes in a corpus (`--corpus`) and a list of words (`--words`) and reads the corpus to print the immediate surrounding context of the given words in the corpus. Optional `--lines` argument specifies the number of lines of concordance should be printed, the default is 20.

## corpus.py
This script takes in cleaned text files (`--input`), tokenizes the files, and outputs (`--corpus`) a corpus of tokenized text files to later be read with PlaintextCorpusReader.

## count.py
This script takes in a corpus (`--corpus`) and prints out the raw count of the desired metric unigrams, bigrams, and trigrams in the corpus.

## freq.py
This script takes in a corpus (`--corpus`) and reports the number of tokens, number of unique tokens, and top 20 most frequent words to an optional output file (`--output`).

## housekeeping.txt
This file reports the number of tokens, unique tokens, and top 20 most frequent tokens of the men's and women's corpora.

## lex_sent.py
This script takes in a corpus (`--corpus`) and performs sentiment analysis on each post in the corpus. It optionally outputs the sentiment reports in a file (`--output`), plots the compound values to check distribution of sentiment (`--plot`), and outputs only the compund scores to a file (`--comp_list`).

## mannwhitneyu.py
This script reads in the compound sentiment scores of two different corpora (`--A` and `--B`).

## run\_clean.py
This file allows a user to run clean.py on an entire folder of raw data files. It takes the input directory file path (`--inp`) and the output directory file path (`--out`) as command line arguments.

## run\_scrape.py
This file allows a user to run scrape.py on multiple forum pages at once. It takes the main forum URL (`--forum`), output directory file path (`--out`), start and end dates (`--start` and `--end`) for the desired time frame, and number of pages (`--pages`) as command-line arguments. This was helpful for BigSoccer scraping since each page of the forum is the [SAME\_URL]/page-[PAGE\_NUMBER].

## scrape.py
This is the script that was used to scrape the raw data from BigSoccer forums. It scrapes post text data from posts within the desired date range originating from threads within the desired date range. It uses the following command line arguments: `--url`, `--out`, `--thread-start`, `--thread-end`, `--post-start`, and `--post-end`.

## select_sent.py
This script takes in a corpus of posts (`--input`), filters the corpus for posts containing keywords and excluding other keywords, and outputs the select corpus (`--output`).

## word_count.py
This script takes in a corpus (`--corpus`) and prints out the number of posts in the corpus, the length of the longest post, the length of the shortest post, the average post length, and the median post length in the corpus.