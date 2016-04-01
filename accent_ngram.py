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

def buildDict(words_dictionary, dictionary_temp):
    # Fill the dictionary
    for iter in dictionary_temp:
        try:
            if (not common.remove_accents(unicode(iter[0])) in words_dictionary):
                words_dictionary[common.remove_accents(unicode(iter[0]))] = [(iter[0],iter[1])]
            else:
                words_dictionary[iter[0]].append((iter[0],iter[1]))

        except:
            sys.exc_info()[0]

def accentWithNgram(buffer, deaccented, padding_char, diff, N, accents,words_dictionary):
    buffer.pop(0)
    buffer.append(deaccented)
    prevText = padding_char.join(buffer[0:diff])
    follText = padding_char.join(buffer[diff+1:N])
    word = buffer[diff]


    # Invoke the shared NGram accent method
    word = common.ngramAccent(word,words_dictionary, diff, accents,prevText, follText, padding_char)
    return word

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ngram", help="N value for N-gram, such as 3 or 5",type=int, default=5)
    parser.add_argument('--timer', dest='timer', help="Timer enabled", action='store_true')
    parser.add_argument('-d', '--dict', dest='dict', help="Dictionary file name", default="../Resources/HU_5gram")
    parser.add_argument('-a', '--accents', type=str, default='áaéeíióoöoőoúuüuűu',
                   help='accent mapping')
    parser.set_defaults(feature=False)
    args = parser.parse_args()

    timer_enabled = args.timer

    accents = args.accents


    # N-gram parameter
    N = args.ngram
    diff = int(math.floor(N/2))

    # Start timer if enabled
    if (timer_enabled):
        start = time.time()

    # Get the dictionary for the ngrams
    dictionary_filename = args.dict

    # Declare the dictionary
    words_dictionary = {}
    dictionary_temp = list(csv.reader(open(dictionary_filename,'r',encoding='utf8'), delimiter='\t'))

    # Build dictionary
    buildDict(words_dictionary, dictionary_temp)

    # Get the shared padding char
    padding_char = common.getPaddingChar()

    buffer = []
    for i in range(0,N):
        buffer.append("")

    initCounter = 0
    # read every line of the input
    for l in stdin:
        #TEXT = l.translate(None, '()?,.:{}[]')
        TEXT = l.decode("utf-8")
        TEXT = TEXT.rstrip('\n')  # strip newline from the end of the line
        TEXT = common.replace(TEXT)
        deaccented = common.remove_accents(unicode(TEXT))
        if (initCounter < diff):
            initCounter += initCounter + 1

        else:
            # Invoke the shared NGram accent method
            word = accentWithNgram(buffer, deaccented, padding_char, diff,N,
                                      accents, words_dictionary)

            print (word)

    # Last ngram_diff iterations
    for i in range(0,diff):
        #Invoke the shared NGram accent method
        word = accentWithNgram(buffer, "", padding_char, diff,N,
                                  accents, words_dictionary)
        print (word)

    # Print timer info
    if (timer_enabled):
        end = time.time()
        print ("Finished in " + str(end-start)+" seconds.")

if __name__ == '__main__':
    main()


