import subprocess
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def page_url(page):
    if page ==1:
        return args.forum
    return f"{args.forum}page-{page}"


def run_page(page):
    output_csv = Path(args.out) / f"page_{page}.csv"

    # skip already done pages
    if output_csv.exists():
        return(f"Already scraped Page {page}")

    url = page_url(page)

    subprocess.run([
        "python3",
        "scrape.py",
        "--url", url,
        "--out", str(output_csv),
        "--thread-start", str(args.start),
        "--thread-end", str(args.end),
        "--post-start", str(args.start),
        "--post-end", str(args.end),
    ])

    return f"Finished Page {page}"

def main():
    pages = range(1, int(args.pages) + 1)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_page, p): p for p in pages}

        for future in as_completed(futures):
            print(future.result())

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--forum", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--pages", required=True)
    args = parser.parse_args()

    output_dir = Path(args.out)
    output_dir.mkdir(exist_ok=True)

    main()
