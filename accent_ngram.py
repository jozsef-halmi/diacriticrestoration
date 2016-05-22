#!/usr/bin/python
# -*- coding: UTF-8 -*-

import operator
import re
import csv
from unicodedata import normalize
import os
from io import open
import xml.etree.ElementTree as ET
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import getopt
import time
import pickle
import argparse
import codecs
import math
from sys import stdin
import unicodedata
from importlib import import_module


# Import common module for shared operations
common = import_module("common")

# Accents word with n-gram solution using local context
def accentWithNgram(buffer, deaccented, padding_char, diff, N, accents,words_dictionary):
    # Remove first unnecessary element
    buffer.pop(0)

    # Append the new one
    buffer.append(deaccented)

    # Create local context
    prevText = padding_char.join(buffer[0:diff])
    follText = padding_char.join(buffer[diff+1:N])
    word = buffer[diff]

    # Invoke the shared NGram accent method
    word = common.ngramAccent(word,words_dictionary, diff, accents,prevText, follText, padding_char)
    return word

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ngram", help="N value for N-gram, such as 1,2,3,4,5..",type=int, default=2)
    parser.add_argument('--timer', dest='timer', help="Timer enabled", action='store_true')
    parser.add_argument('-d', '--dict', dest='dict', help="Dictionary file name", default="../Resources/HU_2gram_dict")
    parser.add_argument('-s', '--dsize', dest='dsize', help="Dictionary size in lines")
    parser.add_argument('-a', '--accents', type=str, default='áaéeíióoöoőoúuüuűu',
                   help='accent mapping')
    parser.set_defaults(feature=False)
    args = parser.parse_args()

    timer_enabled = args.timer

    accents = args.accents
    dictionary_size = int(args.dsize)

    # N-gram parameter
    N = (args.ngram*2)+1
    diff = args.ngram

    # Start timer if enabled
    if (timer_enabled):
        start = time.time()

    # Get the dictionary for the ngrams
    dictionary_filename = args.dict


    # Declare the dictionary
    words_dictionary = {}
    #dictionary_temp = list(csv.reader(open(dictionary_filename,'r',encoding='utf8'), delimiter='\t'))

    # Build dictionary
    common.buildDict(words_dictionary, dictionary_filename, dictionary_size)

    # Get the shared padding char
    padding_char = common.getPaddingChar()

    word_buffer = []
    for i in range(0,N):
        word_buffer.append("")

    initCounter = 0
    # read every line of the input
    for l in stdin:
        #TEXT = l.translate(None, '()?,.:{}[]')
        TEXT = l.decode("utf-8")
        TEXT = TEXT.rstrip('\n')  # strip newline from the end of the line
        if (common.isAccentable(TEXT, accents)):
            TEXT = common.replace(TEXT)
        deaccented = common.remove_accents(unicode(TEXT))
        if (initCounter < diff):
            initCounter += 1
            word_buffer.pop(0)
            word_buffer.append(deaccented)

        else:
            # Invoke the shared NGram accent method
            word = accentWithNgram(word_buffer, deaccented, padding_char, diff,N,
                                      accents, words_dictionary)

            print (word)

    # Last ngram_diff iterations
    for i in range(0,diff):
        #Invoke the shared NGram accent method
        word = accentWithNgram(word_buffer, "", padding_char, diff,N,
                                  accents, words_dictionary)
        print (word)

    # Print timer info
    if (timer_enabled):
        end = time.time()
        print ("Finished in " + str(end-start)+" seconds.")

if __name__ == '__main__':
    main()


