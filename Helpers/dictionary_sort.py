#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from sys import stdin
from collections import defaultdict
import re

def main():
    list = []
    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        words = text.split("\t")
        list.append(words)

    # To return a new list, use the sorted() built-in function...
    #orderedList = sorted(list, key=lambda x: x[1], reverse=True)
    for word, stat in sorted(list,
                                   key=lambda x: x[1], reverse=True):
        print ("{0}\t{1}".format(word.encode('utf-8'),stat))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()