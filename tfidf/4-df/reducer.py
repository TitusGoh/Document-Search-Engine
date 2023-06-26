#!/usr/bin/python3

import sys

unique = {}
for line in sys.stdin:
    term, docid = line.strip().split()
    if term not in unique:
        unique[term] = set()
    unique[term].add(docid)

for term, docid_set in unique.items():
    print('{}\t{}'.format(term, len(docid_set)))