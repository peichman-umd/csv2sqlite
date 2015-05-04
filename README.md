# csv2sqlite
CSV to SQLite conversion tools

## Usage
```
$ csv2sqlite test.db < test.csv

# force creation of the data table, even if it already exists
$ csv2sqlite test.db -f < test.csv

$ sqlite2csv test.db > new.csv
```
