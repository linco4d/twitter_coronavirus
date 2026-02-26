#!/usr/bin/env python3
"""
- We compute per-day hashtag count by summing across languages for that hashtag.
"""

import argparse
import os
import re
import json
import datetime as dt
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outputs_dir",
        default="outputs",
        help="Folder containing mapping outputs (*.lang files). Default: outputs",
    )
    parser.add_argument(
        "--hashtags",
        nargs="+",
        required=True,
        help="One or more hashtags to plot, e.g. --hashtags #coronavirus '#코로나바이러스'",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Optional: restrict to a specific year (e.g., 2020). If omitted, uses all dates found.",
    )
    parser.add_argument(
        "--output_png",
        default="hashtag_timeseries.png",
        help="Where to save the plot PNG. Default: hashtag_timeseries.png",
    )
    return parser.parse_args()

# Matches geoTwitterYY-MM-DD in filenames like:
# geoTwitter20-05-01.zip.lang
DATE_RE = re.compile(r"geoTwitter(\d{2})-(\d{2})-(\d{2})")

def extract_date_from_name(filename: str):
    m = DATE_RE.search(filename)
    if not m:
        return None

    try:
        yy = int(m.group(1))
        mm = int(m.group(2))
        dd = int(m.group(3))
    except ValueError:
        return None

    year = 2000 + yy  # converts 20 → 2020
    try:
        return dt.date(year, mm, dd)
    except ValueError:
        return None

def list_lang_files(outputs_dir: str) -> List[str]:
    # Only scan .lang files from the mapping step
    files = []
    for name in os.listdir(outputs_dir):
        if name.endswith(".lang"):
            files.append(os.path.join(outputs_dir, name))
    return files


def load_json(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


def sum_hashtag_count(day_counts: Dict, hashtag: str) -> int:
    """
    Given the dict loaded from a single .lang file, return total tweets that contain `hashtag`
    by summing across languages.

    If hashtag is missing, returns 0.
    """
    obj = day_counts.get(hashtag)
    if not obj:
        return 0
    # obj is expected to be a dict lang->count
    return int(sum(obj.values()))


def main() -> None:
    args = parse_args()

    outputs_dir = args.outputs_dir
    if not os.path.isdir(outputs_dir):
        raise SystemExit(f"outputs_dir not found or not a directory: {outputs_dir}")

    hashtags = args.hashtags

    # Scan .lang files, extract (date, path)
    dated_files: List[Tuple[dt.date, str]] = []
    for path in list_lang_files(outputs_dir):
        d = extract_date_from_name(os.path.basename(path))
        if d is None:
            continue
        if args.year is not None and d.year != args.year:
            continue
        dated_files.append((d, path))

    if not dated_files:
        year_msg = f" for year {args.year}" if args.year is not None else ""
        raise SystemExit(f"No .lang files with parseable dates found in {outputs_dir}{year_msg}")

    dated_files.sort(key=lambda x: x[0])

    # Build a continuous day range (fill missing days with 0s)
    start_date = dated_files[0][0]
    end_date = dated_files[-1][0]
    all_days: List[dt.date] = []
    cur = start_date
    while cur <= end_date:
        all_days.append(cur)
        cur += dt.timedelta(days=1)

    # Map date -> file path (some days may be missing)
    day_to_path: Dict[dt.date, str] = {d: p for d, p in dated_files}

    # For each hashtag, collect y-values aligned to all_days
    series: Dict[str, List[int]] = {h: [] for h in hashtags}

    for day in all_days:
        path = day_to_path.get(day)
        if path is None:
            # No file for this day; fill zeros
            for h in hashtags:
                series[h].append(0)
            continue

        try:
            counts = load_json(path)
        except Exception:
            # If a per-day output is corrupted, treat as missing
            for h in hashtags:
                series[h].append(0)
            continue

        for h in hashtags:
            series[h].append(sum_hashtag_count(counts, h))

    # Plot
    plt.figure(figsize=(18,6))
    x = list(range(len(all_days)))  # simple numeric x for consistent plotting on servers

    for h in hashtags:
        plt.plot(x, series[h], label=h)
    
        # X-axis labels: exactly 48 evenly spaced ticks, formatted like "Jan 01"
    n_ticks = 48
    total_days = len(all_days)

    if total_days == 0:
        tick_positions = []
    else:
        step = (total_days - 1) / (n_ticks - 1)
        tick_positions = [int(round(i * step)) for i in range(n_ticks)]
        tick_positions[-1] = total_days - 1  # ensure last tick is exact end

    # Remove accidental duplicates from rounding
    tick_positions = sorted(set(tick_positions))

    tick_labels = [all_days[i].strftime("%b %d") for i in tick_positions]

    plt.xticks(tick_positions, tick_labels, rotation=90)
    
    plt.xlabel("Day of year")
    plt.ylabel("Tweets containing hashtag (per day)")
    title_year = f"{args.year} " if args.year is not None else ""
    plt.title(f"{title_year}Hashtag usage over time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output_png)
    plt.close()

    print(f"Scanned {len(dated_files)} daily .lang files from {outputs_dir}")
    print(f"Plotted {len(hashtags)} hashtags from {start_date.isoformat()} to {end_date.isoformat()}")
    print(f"Saved plot: {args.output_png}")


if __name__ == "__main__":
    main()
