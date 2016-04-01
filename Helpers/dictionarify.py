#!/usr/bin/env python2.7

from sys import stdin
from collections import defaultdict
import re

def replace(text):
    for ch in ['\\', ',', '"', '\'', '?',';',':','`','*','_','{','}','[',']','(',')','>','<','#','+','-','.','!','$','\'']:
        text = text.replace(ch," ")

    return text

def main():
    counter = defaultdict(int)

    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        text = replace(text)
        words = text.split()
        for word in words:
            print (word.encode('utf8').strip())


# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()