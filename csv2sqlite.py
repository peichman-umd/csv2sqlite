#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
import csv2sqlite

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest="force", action="store_true")
parser.add_argument('-v', dest="verbose", action="store_true")
parser.add_argument('-d', dest="delimiter", action="store", default=',')
parser.add_argument('db_file')
args = parser.parse_args()

csv2sqlite.convert(sys.stdin, **args.__dict__)
