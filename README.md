# bq-stat integration scripts

These scripts were written for use at [Distilled](https://www.distilled.net/).
They take data from [Stat](https://getstat.com/), and upload that data to
BigQuery. In general, we use this to visualize rankings in Data Studio.

## Things we assume

To use this tool, we assume a Stat account exists with API credentials,
as well as a GCP project where you can upload BigQuery data.

## Things you'll do

### Set up your Stat credentials
```shell
./init
```

This will write your Stat API credentials to a plain text file. The context
these will be used in is assumed to be a machine that runs a cron job to update
client ranking data.

### Create a new client dataset
```shell
./client_init name
```

This command creates a new data set with a client's name as provided. The client
is given an (initially empty) table for ranking data, and a view on that table
defined by the contents of `clustered_legacy.sql`.

### Upload a CSV export directly from Stat
```shell
./fix_utf <infile.csv | ./nld_from_csv.py | ./nld_file_insert name
```

Stat CSV exports are in UTF-16, which breaks BQ's load command. This series of
commands makes the exports UTF-8, then creates a newline-delimited JSON
representation, and finally inserts that JSON into the BQ table for the client
with dataset `name`.

### Update a single client with the latest Stat data
```shell
./client_update name site_id
```

This (without any other side effects or temporary files) gets data from
Stat's API, structures it to match the BQ schema, and inserts it into
the client's ranking table. `site_id` should be the site_id of the 
corresponding Stat project.

### Run a job that updates all clients
```shell
./job
```

If you want to update rankings automatically, `job` can be executed
with cron every day. You'll need to make sure all clients are listed
in `clients.txt`.
