#!/usr/bin/env python2.7

from sys import stdin
from collections import defaultdict


def main():
    counter = defaultdict(int)

    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        text = text.lower()
        words = text.split()
        for word in words:
            counter[word] += 1

    # print counts in decreasing order
    for word, count in sorted(counter.iteritems(),
                                   key=lambda x: -x[1]):
        # printing
        print(u'{0}\t{1}'.format(word, count).encode('utf8'))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()