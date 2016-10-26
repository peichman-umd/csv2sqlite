# csv2sqlite
CSV to SQLite conversion tools

## Usage
```
$ csv2sqlite test.db < test.csv

# force creation of the data table, even if it already exists
$ csv2sqlite test.db -f < test.csv

$ sqlite2csv test.db > new.csv

# round-trip test; the diff should be empty
diff -u test.csv <(./csv2sqlite < test.csv test2.db -f; ./sqlite2csv test2.db)
```

# TODO
- store other dialect parameters of the input csv
- provide the ability to configure the dialect for input or output
