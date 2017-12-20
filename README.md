# bq-stat integration scripts

## Things you'll do

### Set up your credentials
```shell
./init
```

### Create a new client dataset
```shell
./client_init name
```

### Upload a CSV export directly from Stat
```shell
./fix_utf <infile.csv | ./nld_from_csv.py | ./nld_file_insert name
```

### Update a single client with the latest Stat data
```shell
./client_update name site_id
```

### Run a job that updates all clients
```shell
./job
```
