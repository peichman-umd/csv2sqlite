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

### Line Terminators

The `csv2sqlite` utility attempts to determine the line
terminator of the input by checking for CRLF (`0x0D 0x0A`)
or LF (`OxOA`) in the input CSV data. If it finds at least one
CRLF, it uses CRLF as the line terminator. Otherwise, it uses
LF. This setting is saved in the dialect table of the database
with the key `lineterminator`.

### Delimiters

The default delimiter is a comma, but this can be changed
using the `-d` switch. For example, to read a file that uses
pipes as its delimiter character:

```
$ csv2sqlite pipes.db -d '|' <pipes.txt
```

Note the quoting of the delimiter argument. To specify a TAB
character as a delimiter, you have two options. If you using Bash or another shell that supports it, you may use an [ANSI
C-like escaped string][escaped-string] to pass a literal TAB
(`0x09`) character:

```
$ csv2sqlite tabs.db -d $'\t' <tabs.txt
```

Since you may be on a platform that doesn't support this
style, this utility also recognizes a literal `\t` and
converts it into a TAB internally:

```
$ csv2sqlite tabs.db -d '\t' <tabs.txt
```

The specified delimiter is saved in the dialect table of the
database under the key `delimiter`. It is used by `sqlite2csv`
to recreate a (hopefully) byte-for-byte identical CSV file to
the original.


# TODO
- store other dialect parameters of the input csv
- provide the ability to configure the dialect for input or output
- support CSV files without headers
- configurable table names

[escaped-string]: http://wiki.bash-hackers.org/syntax/quoting#ansi_c_like_strings
