#!/usr/bin/env python
# coding=utf-8

from sys import stdin
import csv
import json

def map_row_to_schema(row):
    return {
        "timestamp": row["Date"] + " 00:00",
        "keyword": row["Keyword"],
        "market": row["Market"],
        "location": row["Location"],
        "device": row["Device"],
        "rank": row["Rank"],
        "base_rank": row["Rank"],
        "url": row["URL"] if row["URL"] else None,
        "advertiser_competition": row["Advertiser Competition"],
        "gms": row["Global Monthly Searches"],
        "rms": row["Regional Monthly Searches"],
        "cpc": row["CPC"],
        "tags": [tag.strip() for tag in row["Tags"].split("/")] if row["Tags"] else [],
    }

def csv_reader():
    return csv.DictReader(stdin, delimiter="\t")

def main():
    for row in csv_reader():
        print(json.dumps(map_row_to_schema(row)))

if __name__ == "__main__":
    main()
