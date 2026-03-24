import argparse
import re
import csv
import inflect
from langdetect import detect
import contractions

# regex for various things
quote_pattern = re.compile(r'.*? said:.*?click to expand\.\.\.')
url_pattern = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)
twit_pattern = re.compile(r'pic\.twitter\.com/\S+')
extra_click = re.compile(r'^.*click to expand\.\.\.')
tweet_pattern = re.compile(r'\d+\s+is not a valid tweet id')

# handle ordinals
p = inflect.engine()
ordinal_pattern = re.compile(r'\b(\d+)(st|nd|rd|th)\b')

# clean the lines of raw text passed in
def clean(raw_text):
    text = raw_text.lower() # lowercase
    text = re.sub(twit_pattern, '', text) # no twitter links
    text = re.sub(url_pattern, '', text) # no urls
    text = re.sub(quote_pattern, '', text) # no BigSoccer reply pattern
    text = re.sub(extra_click, '', text) # no extra "Click to expand..."
    text = re.sub(tweet_pattern, '', text) # remove "not a valid tweet id"
    text = re.sub(ordinal_pattern, lambda m: p.number_to_words(m.group(0)), text) # replace ordinals with words
    text = re.sub(r'@\w+', ' ', text) # no @s
    text = re.sub(r'#\w+', ' ', text) # no #s
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # no non-ASCII
    text = re.sub(r"[^a-z0-9\s']", ' ', text) # no non-alphanumeric or '
    clean_text = re.sub(r'\s+', ' ', text) # normalize spaces
    return clean_text

def eng(text):
    try:
        return text if detect(text) == "en" else ""
    except:
        return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pass raw data to be cleaned!")
    parser.add_argument("--inp", required=True, help="Input file path")
    parser.add_argument("--out", required=True, help="Output file path")
    
    args = parser.parse_args()
    
    with open(args.inp, newline='', encoding="utf-8", errors='ignore') as f, open(args.out, "w", encoding="utf-8") as out:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for row in reader:
            if not row:
                continue

            raw_text = row[1]
            raw_eng = eng(raw_text) # remove all non-english entries
            no_con = contractions.fix(raw_eng) # expand all non-'s contractions
            clean_text = clean(no_con) # clean the text
            if clean_text:
                out.write(clean_text + "\n\n") # output as txt
