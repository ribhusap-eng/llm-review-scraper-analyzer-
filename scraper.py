

import requests
import csv
import time
import sys
from datetime import datetime, timezone


APP_ID    = "292030"          
GAME_NAME = "The Witcher 3: Wild Hunt"
TARGET    = 600              
OUTPUT    = "steam_reviews.csv"

# ──────────────────────────────────────────────

BASE_URL = f"https://store.steampowered.com/appreviews/{APP_ID}"

PARAMS = {
    "json"          : 1,
    "filter"        : "recent",     
    "language"      : "english",
    "num_per_page"  : 100,          
    "review_type"   : "all",        
    "purchase_type" : "all",
    "cursor"        : "*",          
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (academic research scraper)"
}


def fetch_page(cursor: str) -> dict:
    """Fetch one page of reviews from Steam and return raw JSON."""
    PARAMS["cursor"] = cursor
    try:
        r = requests.get(BASE_URL, params=PARAMS, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Network error: {e}")
        return {}


def parse_review(raw: dict) -> dict:
    """Convert one raw Steam review dict into our CSV-friendly dict."""
    ts      = raw.get("timestamp_created", 0)
    date    = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    rating  = "Positive" if raw.get("voted_up") else "Negative"
    text    = raw.get("review", "").replace("\n", " ").replace("\r", " ").strip()
    steamid = raw["author"]["steamid"]         
    url     = f"https://store.steampowered.com/app/{APP_ID}/#app_reviews_hash"

    return {
        "item_name"   : GAME_NAME,
        "review_date" : date,
        "rating"      : rating,
        "username"    : steamid,
        "review_text" : text,
        "source_url"  : url,
    }


def print_progress(page: int, batch_size: int, new: int, total: int, cursor_changed: bool):
    bar_len   = 30
    filled    = int(bar_len * total / TARGET)
    bar       = "█" * filled + "░" * (bar_len - filled)
    pct       = min(100, int(100 * total / TARGET))
    print(
        f"  Page {page:>3} │ batch={batch_size:<3} new={new:<3} "
        f"│ [{bar}] {pct:>3}%  ({total}/{TARGET})  "
        f"│ cursor_advanced={'YES' if cursor_changed else 'NO'}"
    )


def main():
    print("=" * 65)
    print(f"  Steam Review Scraper")
    print(f"  Game    : {GAME_NAME}  (App ID: {APP_ID})")
    print(f"  Target  : {TARGET} unique reviews")
    print(f"  Output  : {OUTPUT}")
    print("=" * 65)

    seen_ids      : set  = set()
    all_reviews   : list = []
    cursor        : str  = "*"
    page          : int  = 0
    consecutive_empty     = 0   
    MAX_CONSECUTIVE_EMPTY = 3   

    fieldnames = ["item_name", "review_date", "rating",
                  "username", "review_text", "source_url"]

    with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
     
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while len(all_reviews) < TARGET:
            data = fetch_page(cursor)

            if not data:
                print("  [STOP] Empty API response – aborting.")
                break

            if not data.get("success", False):
                print("  [STOP] Steam API returned success=false.")
                break

            batch      = data.get("reviews", [])
            new_cursor = data.get("cursor", cursor)
            page      += 1

            
            new_count = 0
            for raw in batch:
                rid = raw.get("recommendationid")
                if rid in seen_ids:
                    continue                          
                if not raw.get("review", "").strip(): 
                    continue
                seen_ids.add(rid)
                parsed = parse_review(raw)
                all_reviews.append(parsed)
                writer.writerow(parsed)
                new_count += 1
                if len(all_reviews) >= TARGET:
                    break

            cursor_advanced = (new_cursor != cursor)
            print_progress(page, len(batch), new_count, len(all_reviews), cursor_advanced)

           
            if not cursor_advanced:
                print("  [STOP] Cursor did not advance → end of Steam results.")
                break

            if new_count == 0:
                consecutive_empty += 1
                print(f"  [WARN] No new reviews this page "
                      f"({consecutive_empty}/{MAX_CONSECUTIVE_EMPTY} allowed).")
                if consecutive_empty >= MAX_CONSECUTIVE_EMPTY:
                    print("  [STOP] Too many consecutive empty pages – stopping.")
                    break
            else:
                consecutive_empty = 0  

            cursor = new_cursor
            time.sleep(0.75)   
                               
    print()
    print("=" * 65)
    print(f"  DONE")
    print(f"  Unique reviews saved : {len(all_reviews)}")
    print(f"  Total IDs tracked    : {len(seen_ids)}")
    print(f"  Pages fetched        : {page}")
    print(f"  Output file          : {OUTPUT}")
    print("=" * 65)

    if len(all_reviews) < TARGET:
        print(f"\n  NOTE: Only {len(all_reviews)} reviews collected (target was {TARGET}).")
        print("  This means Steam has fewer English reviews than your target,")
        print("  OR the game's review count is lower than expected.")
        print("  Try APP_ID 570 (Dota 2) for virtually unlimited reviews.")
    else:
        print(f"\n  SUCCESS: {TARGET}+ unique reviews collected!")


if __name__ == "__main__":
    main()