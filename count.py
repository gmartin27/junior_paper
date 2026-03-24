from nltk.corpus import PlaintextCorpusReader as corp_reader
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.util import bigrams
from nltk.util import trigrams
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    args = parser.parse_args()
    tok = RegexpTokenizer(r"[A-Za-z]+(?:'[A-Za-z]+)?")

    corpus = corp_reader(args.corpus, r".*\.txt", word_tokenizer=tok)
    tokens = corpus.words()
    size = len(tokens)

    freq_dist = FreqDist(tokens)
    
    inf = ["girl", "girls", "boy", "boys", "lady", "ladies", "lad", "lads", "kids"]
    gen = ["male", "female", "women's", "men's", "usmnt", "uswnt"]
    kin = ["mother", "father", "married", "child", "children", "pregnant", "mom", "dad"]
    quant = ["bad", "worst", "terrible", "good", "great", "best"]
    acro = ["ussf", "wnt", "mnt", "mls", "nwsl", "wc", "wwc", "mwc"]
    wnames = ["alyssa", "naeher", "thompson", "naomi", "girma", "julie", "ertz", "lindsey", "horan", 
              "sophia", "smith", "huerta", "alex", "morgan", "emily", "sonnet", "andi", "sullivan", 
              "crystal", "dunn", "trinity", "rodman", "fox", "megan", "rapinoe", "rose", 
              "lavelle", "kelley", "o'hara", "vlatko", "andonovski", "emma", "hayes", "carli", "lloyd"]
    mnames = ["christian", "pulisic", "tim", "ream", "weston", "mckennie", "walker", 
              "zimmerman", "tyler", "adams", "antonee", "robinson", "weah", "matt", 
              "turner", "sergino", "dest", "yunus", "musah", "jesus", "ferreira", "gregg", 
              "berhalter", "gio", "reyna"]

    mets = [inf, gen, kin, quant, acro, wnames, mnames]

    print(f"corpus file: {args.corpus}")
    for words in mets:
        for word in words:
            print(f"Occurrences of {word}: {freq_dist[word]} out of {size}")
    
    bi = bigrams(tokens)
    bi_freq = FreqDist(bi)

    bis = [("world", "cup"), ("national", "team"), ("us", "soccer"),("women's", "player"), ("men's", "player"), 
           ("female", "player"), ("male", "player"), ("women's", "team"),("men's", "team"), ("alyssa", "naeher"), 
           ("alyssa", "thompson"),("naomi", "girma"), ("julie", "ertz"), ("lindsey", "horan"), 
           ("sophia", "smith"), ("sophia", "huerta"), ("alex", "morgan"), ("emily", "sonnet"), ("andi", "sullivan"), 
           ("crystal", "dunn"), ("trinity", "rodman"), ("emily", "fox"), ("megan", "rapinoe"), ("rose", "lavelle"),
           ("kelley", "o'hara"), ("vlatko", "andonovski"), ("emma", "hayes"), ("carli", "lloyd"), 
           ("christian", "pulisic"), ("tim", "ream"), ("weston", "mckennie"), ("walker", "zimmerman"),
           ("tyler", "adams"), ("antonee", "robinson"), ("tim", "weah"), ("matt", "turner"), ("sergino", "dest"), 
           ("yunus", "musah"), ("jesus", "ferreira"), ("gregg", "berhalter"), ("gio", "reyna")]

    for bi in bis:
        print(f"Occurences of {bi}: {bi_freq[bi]}")

    tri = trigrams(tokens)
    tri_freq = FreqDist(tri)
    print(tri_freq.most_common(10))

    tris = [("women's", "world", "cup"), ("men's", "world", "cup"), ("women's", "national", "team"), 
            ("men's", "national", "team")]

    for tri in tris:
        print(f"Occurences of {tri}: {tri_freq[tri]}")

    for tri in tris:
        print(tri_freq[tri])
