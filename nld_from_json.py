#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
from sys import stdin
import json

def map_row_to_schema(row):
    return {
        "timestamp": datetime.now().isoformat(),
        "keyword": row["Keyword"],
        "market": row["KeywordMarket"],
        "location": row["KeywordLocation"] if row["KeywordLocation"] else "",
        "device": row["KeywordDevice"],
        "rank": row["KeywordRanking"]["Google"]["Rank"] if row["KeywordRanking"] else None,
        "base_rank": row["KeywordRanking"]["Google"]["BaseRank"] if row["KeywordRanking"] else None,
        "url": row["KeywordRanking"]["Google"]["Url"] if row["KeywordRanking"] else None,
        "advertiser_competition": row["KeywordStats"]["AdvertiserCompetition"] if row["KeywordRanking"] else None,
        "gms": row["KeywordStats"]["GlobalSearchVolume"] if row["KeywordStats"] else None,
        "rms": row["KeywordStats"]["RegionalSearchVolume"] if row["KeywordStats"] else None,
        "cpc": row["KeywordStats"]["CPC"] if row["KeywordStats"] else None,
        "tags": [] if row["KeywordTags"] == "none" else map(lambda str: str.strip(), row["KeywordTags"].split(',')),
    }

def main():
    for row in json.load(stdin)["Response"]["Result"]:
        print(json.dumps(map_row_to_schema(row)))

if __name__ == "__main__":
    main()
