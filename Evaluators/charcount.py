#!/usr/bin/env python2.7


from sys import stdin
from collections import defaultdict


def main():
    counter = defaultdict(int)
    charCount = 0
    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        for character in text:
            counter[character] += 1
            charCount += 1

    # print counts in decreasing order
    for character, count in sorted(counter.iteritems(),
                                   key=lambda x: -x[1]):
        percentage = 100*count /float(charCount)
        print(u'{0}\t{1}'.format(character, (percentage)).encode('utf8'))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()