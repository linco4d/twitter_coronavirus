#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--output_folder', default='outputs')
args = parser.parse_args()

# imports
import os
import zipfile
import datetime
import json
from collections import Counter, defaultdict
import zlib

# hard-coded hashtags
hashtags = [
    '#코로나바이러스',  # korean
    '#コロナウイルス',  # japanese
    '#冠状病毒',        # chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',
]

# normalize ASCII hashtags for matching
hashtags = [h.lower() for h in hashtags]

# initialize counters
counter_lang = defaultdict(Counter)
counter_country = defaultdict(Counter)

UNKNOWN_COUNTRY = "__unknown__"

zip_files = []

if os.path.isdir(args.input_path):
    for fname in sorted(os.listdir(args.input_path)):
        if fname.startswith("geoTwitter20") and fname.endswith(".zip"):
            zip_files.append(os.path.join(args.input_path, fname))
else:
    zip_files.append(args.input_path)

if not zip_files:
    print("No matching zip files found.")
    exit(1)

for zip_path in zip_files:
    print("Processing zip:", zip_path)

    try:
        with zipfile.ZipFile(zip_path) as archive:
            for filename in archive.namelist():
                print(datetime.datetime.now(), zip_path, filename)

                try:
                    with archive.open(filename) as f:
                        line_i = 0
                        for line in f:
                            line_i += 1
                            if line_i % 1_000_000 == 0:
                                print(datetime.datetime.now(), filename, "lines:", line_i)

                            try:
                                tweet = json.loads(line)
                            except json.JSONDecodeError:
                                continue

                            lang = tweet.get('lang')
                            if not lang:
                                continue

                            text = tweet.get('text', '').lower()

                            place = tweet.get('place') or {}
                            country = place.get('country_code') or UNKNOWN_COUNTRY

                            counter_lang['_all'][lang] += 1
                            counter_country['_all'][country] += 1

                            for hashtag in hashtags:
                                if hashtag in text:
                                    counter_lang[hashtag][lang] += 1
                                    counter_country[hashtag][country] += 1

                except (zipfile.BadZipFile, zlib.error, OSError) as e:
                    print("WARNING: skipping corrupted member:", filename, "error:", str(e))
                    continue

    except (zipfile.BadZipFile, OSError) as e:
        print("WARNING: skipping corrupted zip:", zip_path, "error:", str(e))
        continue

# write outputs
os.makedirs(args.output_folder, exist_ok=True)

if os.path.isdir(args.input_path):
    base_name = os.path.basename(os.path.abspath(args.input_path))
else:
    base_name = os.path.basename(args.input_path)

output_path_base = os.path.join(args.output_folder, base_name)

output_path_lang = output_path_base + '.lang'
print('saving', output_path_lang)
with open(output_path_lang, 'w') as f:
    json.dump(counter_lang, f)

output_path_country = output_path_base + '.country'
print('saving', output_path_country)
with open(output_path_country, 'w') as f:
    json.dump(counter_country, f)

