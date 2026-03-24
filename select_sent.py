import os
import shutil
import argparse

INCLUSION_WORDS = ['usmnt', 'uswnt', 'wwc', 'wc', 'team', 'player', 'teams', 'players', 'cup', 'formation', 'performance', 'coach', 'coaches', 'tactics', 'alyssa', 'naeher', 'thompson', 'naomi', 'girma', 'julie', 'ertz', 'lindsey', 'horan', 'sophia', 'smith', 'alex', 'morgan', 'emily', 'sonnet', 'andi', 'sullivan', 'crystal', 'dunn', 'trinity', 'rodman', 'fox', 'megan', 'rapinoe', 'rose', 'lavelle', 'kelley', 'ohara', 'vlatko', 'andonovski', 'emma', 'hayes', 'carli', 'lloyd', 'christian', 'pulisic', 'tim', 'ream', 'weston', 'mckennie', 'walker', 'zimmerman', 'tyler', 'adams', 'antonee', 'robinson', 'weah', 'matt', 'turner', 'sergino', 'dest', 'yunus', 'musah', 'jesus', 'ferreira', 'gregg', 'berhalter', 'gio', 'reyna', 'huerta']

EXCLUSION_WORDS = ["killings"]

def filter_dir(out, inp):
    if not os.path.exists(out):
        os.makedirs(out)

    file_count = 0
    match_count = 0

    for file in os.listdir(inp):
        if file.endswith(".txt"):
            file_count += 1
            file_path = os.path.join(inp, file)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()

                contains_inclusion = any(word in content for word in INCLUSION_WORDS)
                contains_exclusion = any(word in content for word in EXCLUSION_WORDS)

                if contains_inclusion and not contains_exclusion:
                    shutil.copy(file_path, os.path.join(out, file))
                    match_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    filter_dir(args.output, args.input)
