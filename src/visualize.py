#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
parser.add_argument('--output_path', default='output.png')
args = parser.parse_args()

# imports
import json
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

if args.key not in counts:
    raise ValueError(f"Key '{args.key}' not found in input file")

# normalize the counts by total values (optional)
if args.percent:
    for k in counts[args.key]:
        if k in counts['_all'] and counts['_all'][k] != 0:
            counts[args.key][k] /= counts['_all'][k]

# sort low → high and take top 10
items = sorted(counts[args.key].items(), key=lambda item: item[1])
top10 = items[-10:]  # highest 10, still low→high order

keys = [k for k, v in top10]
values = [v for k, v in top10]

# create bar chart
plt.figure()
plt.bar(keys, values)
plt.xticks(rotation=45)
plt.xlabel("Keys")
plt.ylabel("Value")
plt.title(f"{args.key} {'(percent)' if args.percent else '(count)'}")
plt.tight_layout()

# save figure
plt.savefig(args.output_path)
plt.close()

print(f"Saved bar graph to {args.output_path}")
