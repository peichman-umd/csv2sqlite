#!/usr/bin/env python

from __future__ import print_function

import csv
import sqlite3
import sys
import argparse
import re

# source: http://stackoverflow.com/a/6701665/5124907
import codecs

def quote_identifier(s, errors="strict"):
    encodable = s.encode("utf-8", errors).decode("utf-8")

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError("NUL-terminated utf-8", encodable,
                                   nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return '"' + encodable.replace('"', '""') + '"'

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest="FORCE", action="store_true")
parser.add_argument('-v', dest="VERBOSE", action="store_true")
parser.add_argument('-d', dest="DELIMITER", action="store", default=',')
parser.add_argument('DB_FILE')
args = parser.parse_args()

dbh = sqlite3.connect(args.DB_FILE)

# attempt to automatically detect line endings
sample = sys.stdin.read(1024)
dialect = {}
sys.stdin.seek(0)
# explicitly check the line terminator, since the csv dialect sniffer
# always seems to return '\r\n', even if the source file only has '\n'
if re.search(r"\x0d\x0a", sample):
    # DOS
    dialect['lineterminator'] = "\x0d\x0a"
else:
    # Unix
    dialect['lineterminator'] = "\x0a"

# set delimiter character from argument
dialect['delimiter'] = args.DELIMITER
# allow the literal string \t to stand for a TAB
if dialect['delimiter'] == '\\t':
    dialect['delimiter'] = '\t'

in_reader = csv.reader(sys.stdin, **dialect)

# save dialect attributes
if args.FORCE:
    dbh.execute('drop table if exists dialect')
dbh.execute('create table dialect (key text, value text)')
for key in dialect:
    dbh.execute('insert into dialect (key, value) values (?, ?)', (key, dialect[key]))
if args.VERBOSE:
    print(dialect, file=sys.stderr)

# read header line
headers = in_reader.next()
if args.VERBOSE:
    print(headers, file=sys.stderr)

# transform header strings to legal SQL identifiers
# for use as column names
columns = [ quote_identifier(h) for h in headers ]

# preserve original header names and positions
if args.FORCE:
    dbh.execute('drop table if exists headers')
dbh.execute('create table headers (position text, header text, column text)')
dbh.executemany(
    'insert into headers (position, header, column) values (?,?,?)',
    zip(
        list(xrange(1,len(headers) + 1)),
        headers,
        columns,
    ),
)

sql_create = 'create table data (' + ','.join([c + ' text' for c in columns]) + ')'
if args.VERBOSE:
    print(sql_create, file=sys.stderr)
if args.FORCE:
    dbh.execute('drop table if exists data')
dbh.execute(sql_create)

placeholders = ['?'] * (len(columns) + 1)
sql_insert = 'insert into data (rowid,' + ','.join(columns) + ') values (' + ','.join(placeholders) + ')'
if args.VERBOSE:
    print(sql_insert, file=sys.stderr)

for row in in_reader:
    data_row = [in_reader.line_num] + row
    if args.VERBOSE:
        print(data_row, file=sys.stderr)
    dbh.execute(sql_insert, tuple(data_row))

dbh.commit()
