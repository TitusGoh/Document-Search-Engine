#!/usr/bin/python3

import sys

for line in sys.stdin:
    key, count = line.strip().split()
    doc_id, term = key.split('+')

    print('{}\t{}\t{}'.format(doc_id, term, count))