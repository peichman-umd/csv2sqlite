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
- store original line numbers
- store original line endings (and other dialect parameters) of the input csv
- ensure that sqlite2csv prints out the data in the correct column order
