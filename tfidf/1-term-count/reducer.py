#!/usr/bin/python3

import sys

newKey = None
newCount = 0
for line in sys.stdin:
    key, count = line.strip().split()
    count = int(count)

    if key != newKey:
        #for the first iteration when oldKey is null
        if newKey:
            print('{}\t{}'.format(newKey, newCount))
        newKey = key
        newCount = 0
    
    newCount += count

#print last term
print('{}\t{}'.format(newKey, newCount))