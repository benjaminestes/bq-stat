#!/usr/bin/env python
# coding=utf-8

"""Given a CSV file from Stat's ranking ranking export, create a
newline-delimited JSON file corresponding with BQ schema."""

from sys import stdin
import csv
import json


def map_row_to_schema(row):
    """Associate a value from a Stat CSV export with the correct
    identifier from BQ schema.

    When first adding a client to this system we may have historical data
    that we want to import. That data comes from Stat's ranking export.
    We need to map values from Stat's data into the schema we've design
    to interface with Data Studio. This function handles that mapping.

    Args:
        row: A dict extracted from Stat's ranking CSV, that
            corresponds with a single observation of a keyword ranking.

    Returns:
        A dict representing data for a single keyword observation that
        complies with the BQ schema of our client tables.

        Keys that were missing from Stat's response get None/NULL values.
    """
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
    """If called from shell, assume Stat CSV file is fed from stdin.

    Returns:
        An iterable yielding a dict for each row in the Stat CSV.
    """
    return csv.DictReader(stdin, delimiter="\t")


def main():
    """Creat an object corresponding to Stat's CSV export,
    and write a JSON object for each observation in Stat's response."""

    # Stat's API outputs a single row for each instance of a keyword,
    # in the sense you'd take it looking at their GUI. That means only
    # a single ranking page is included.
    #
    # However, this script is for importing historical data which we
    # get from a ranking export. The ranking export is a CSV which
    # includes a row for each ranking page.  It will also include an
    # empty row for an observation of no ranking page. We want to make
    # sure at most a single observation is included to match what we
    # get from the API.
    #
    # This emits a line for the first instance of a "key". By default
    # this will be the best-ranking page. However, Stat could change
    # this in the future.
    
    seen = set()
    
    for row in csv_reader():
        r = map_row_to_schema(row)
        
        key = (r["timestamp"],
               r["keyword"],
               r["market"],
               r["location"],
               r["device"])

        if key not in seen:
            seen.add(key)
            print(json.dumps(r))


if __name__ == "__main__":
    main()
