#!/usr/bin/env python
# coding=utf-8

"""Given a JSON response from Stat's ranking API, create a
newline-delimited JSON file corresponding with BQ schema."""

from datetime import datetime
from sys import stdin
import json


def map_row_to_schema(row):
    """Associate a value from a Stat JSON object with the correct
    identifier from BQ schema.

    Daily ranking updates come from Stat's JSON API. This export is complex.
    We need to map values from Stat's data into the schema we've design
    to interface with Data Studio. This function handles that mapping.

    Args:
        row: A JSON object extracted from Stat's JSON API response, that
            corresponds with a single observation of a keyword ranking.

    Returns:
        A dict representing data for a single keyword observation that
        complies with the BQ schema of our client tables.

        Keys that were missing from Stat's response get None/NULL values.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "keyword": row["Keyword"],
        "market": row["KeywordMarket"],
        "location": row["KeywordLocation"] if row["KeywordLocation"] else "",
        "device": row["KeywordDevice"],
        "rank": row["KeywordRanking"]["Google"]["Rank"] if row["KeywordRanking"] else None,
        "base_rank": row["KeywordRanking"]["Google"]["BaseRank"] \
                if row["KeywordRanking"] else None,
        "url": row["KeywordRanking"]["Google"]["Url"] if row["KeywordRanking"] else None,
        "advertiser_competition": row["KeywordStats"]["AdvertiserCompetition"] \
            if row["KeywordRanking"] else None,
        "gms": row["KeywordStats"]["GlobalSearchVolume"] if row["KeywordStats"] else None,
        "rms": row["KeywordStats"]["RegionalSearchVolume"] \
                if row["KeywordStats"] else None,
        "cpc": row["KeywordStats"]["CPC"] if row["KeywordStats"] else None,
        "tags": [] if row["KeywordTags"] == "none" else \
            map(lambda str: str.strip(), row["KeywordTags"].split(',')),
    }


def main():
    """If called from shell, assume Stat JSON response comes from stdin,
    and write a JSON object for each observation in Stat's response."""
    for row in json.load(stdin)["Response"]["Result"]:
        print(json.dumps(map_row_to_schema(row)))


if __name__ == "__main__":
    main()
