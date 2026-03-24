import argparse
import csv
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BASE_URL = "https://bigsoccer.com"
MAX_WORKERS = 5

session = requests.Session()


def parse_thread_date(date_str: str) -> datetime:
    return datetime.strptime(date_str.strip(), "%b %d, %Y")


def get_last_page(soup):
    nav = soup.select_one("div.PageNav")
    if nav and nav.get("data-last"):
        return int(nav["data-last"])
    return 1


def build_thread_pages(thread_url, last_page):
    return [thread_url] + [
        f"{thread_url}page-{i}" for i in range(2, last_page + 1)
    ]

def scrape_thread_page(url, post_start_dt, post_end_dt):
    collected = []

    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
    except requests.RequestException:
        return collected

    soup = BeautifulSoup(r.text, "html.parser")

    for msg in soup.select("li.sectionMain.message"):
        content = msg.select_one("div.messageContent")
        date_tag = msg.select_one("a.datePermalink span.DateTime")
        if not content or not date_tag or not date_tag.has_attr("title"):
            continue

        try:
            post_dt = datetime.strptime(date_tag["title"], "%b %d, %Y at %I:%M %p")
        except Exception:
            continue

        if post_start_dt <= post_dt <= post_end_dt:
            collected.append({
                "post_date": post_dt,
                "raw_post": content.get_text(" ", strip=True)
            })

    return collected

def scrape_forum(forum_url, output_file, delay, thread_start_dt, thread_end_dt, post_start_dt, post_end_dt):
    output = []

    print(f"Fetching forum page: {forum_url}")

    r = session.get(forum_url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    threads = []
    # Collect thread URLs and start dates from forum page
    for div in soup.select("div.titleText"):
        a_tag = div.select_one("h3.title a")
        date_tag = div.select_one("span.DateTime")
        if not a_tag or not date_tag:
            continue
        thread_url = urljoin(BASE_URL, a_tag["href"])
        thread_date = parse_thread_date(date_tag.get_text())
        threads.append((thread_url, thread_date))

    print(f"Found {len(threads)} threads on page")

    # Filter threads by start date
    threads = [(url, dt) for url, dt in threads if thread_start_dt <= dt <= thread_end_dt]

    print(f"{len(threads)} threads within date range")

    for idx, (thread_url, dt) in enumerate(threads, 1):
        print(f"[{idx}/{len(threads)}] Scraping thread: {thread_url} (OP date: {dt.date()})")

        last_page = 1
        try:
            r = session.get(thread_url, timeout=30)
            r.raise_for_status()
            thread_soup = BeautifulSoup(r.text, "html.parser")
            last_page = get_last_page(thread_soup)
        except requests.RequestException:
            print("Failed to fetch thread")
            continue

        page_urls = build_thread_pages(thread_url, last_page)

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(scrape_thread_page, url, post_start_dt, post_end_dt) for url in page_urls]
            for future in as_completed(futures):
                posts = future.result()
                output.extend(posts)

        time.sleep(delay)

    if len(output) > 0:
        print(f"Writing {len(output)} posts to {output_file}")
        df = pd.DataFrame(output)
        df.to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape BigSoccer threads")
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--thread-start", required=True)
    parser.add_argument("--thread-end", required=True)
    parser.add_argument("--post-start", required=True)
    parser.add_argument("--post-end", required=True)
    args = parser.parse_args()

    scrape_forum(
        forum_url=args.url,
        output_file=args.out,
        delay=args.delay,
        thread_start_dt=datetime.fromisoformat(args.thread_start),
        thread_end_dt=datetime.fromisoformat(args.thread_end),
        post_start_dt=datetime.fromisoformat(args.post_start),
        post_end_dt=datetime.fromisoformat(args.post_end),
    )

