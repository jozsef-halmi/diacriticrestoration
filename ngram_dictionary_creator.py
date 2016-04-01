#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from sys import stdin
from collections import defaultdict
import argparse
import re

from importlib import import_module

def main():
    # Import common module for shared operations
    common = import_module("common")

    # Read input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n", help="N number",type=int, default=5)
    parser.add_argument('-a', '--accents', type=str, default='áaéeíióoöoőoúuüuűu',
                   help='accent mapping')
    parser.set_defaults(feature=False)
    args = parser.parse_args()

    # Variables associated with the N-value
    n_number = args.n
    n_halflength = int(round(n_number/2))

    # Variables associated with the accents
    #accent_map = convert_mapping(args.accents)
    #accent_set = set(accent_map.iterkeys())

    accent_string = args.accents.decode('utf8')
    accent_string = accent_string + accent_string.upper()
    #print ("Accent string: "+accent_string)
    counter = defaultdict(int)
    padding_char = common.getPaddingChar()
    empty_string = n_number*padding_char


    buffer = []
    for i in range(0,n_number):
        buffer.append("")

    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        text = common.replace(text)
        #text = n_halflength * ' ' + text + n_halflength * ' '
        text = text.lower()
        text = re.sub(u'[^a-zA-Z0-9'+accent_string+'\n\.]', padding_char, text)

        buffer.pop(0)
        buffer.append(text)

        prevText = padding_char.join(buffer[0:n_halflength])
        follText = padding_char.join(buffer[n_halflength+1:n_number])
        word = buffer[n_halflength]

        wordStartIndex = len(prevText)
        wordEndIndex = len(prevText) + len(word) + 1

        fullText = prevText + padding_char + word + padding_char + follText

        for index in range (wordStartIndex,wordEndIndex):
           if (fullText[index-n_halflength:index+n_halflength+1] != empty_string
                # This selects substrings only with accentable characters in the middle
                and fullText[index:index+1] in accent_string):
                counter[fullText[index-n_halflength:index+n_halflength+1]] +=1
                #print ("The word is: "+text[index-n_halflength:index+n_halflength+1])
                #print ("The middle is: "+text[index:index+1])


    for character, count in sorted(counter.iteritems(),
                                   key=lambda x: -x[1]):
        # printing
        print(u'{0}\t{1}'.format(character, count).encode('utf8'))

# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()