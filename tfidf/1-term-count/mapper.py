#!/usr/bin/python3

import sys
import os

for line in sys.stdin:
    docid = os.path.splitext(
        os.path.basename(
        os.getenv('map_input_file')))[0]
    for word in line.strip().split():
        lower = word.lower()
        term = "".join(filter(lambda ch: 97 <= ord(ch) <= 122, lower))
        if len(term):
            print('{}+{}\t{}'.format(docid, term, 1))