#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function


import operator
from io import open
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import argparse
from sys import stdin
import time
import math
import unicodedata
from importlib import import_module

# Import common module for shared operations
common = import_module("common")

# Deaccents a single word
def deaccent( word ):
    return common.remove_accents(unicode(word))

# Sorts tuple
def sortTupleArray ( array, index ):
    array.sort(key=operator.itemgetter(index))
    return array;



# Returns the candidate for a given word
def findCandidate ( inputWord, words_dictionary):
    if (inputWord in words_dictionary):
        return words_dictionary[inputWord]
    return ""

# Corrects cases, for example:
# Peter, péter -> Péter
# LIFE, life -> LIFE
def correctCases( original, corrected ):
    markCases = [];

    for char in original:
        if (char.upper() == char):
            markCases.append('u')
        else:
            markCases.append('l')

    # Now an array like this exists: ['u', 'l', 'l', 'l', 'l']
    outArray = []
    index = 0
    for mark in markCases:
        if (index < len(corrected)):
            if (mark == 'u'):
                outArray.append(corrected[index].upper())
            else:
                outArray.append(corrected[index].lower())

        index = index+1


    corrected = ''.join(outArray)
    #print ('original: '+ original + ', corrected: '+corrected)
    return corrected;

# Accentises a word
def accent(deaccented_input, words_dictionary):
    istitle = (deaccented_input.istitle())
    word = findCandidate(deaccented_input.lower(), words_dictionary)
    if (word == ""):
        return (deaccented_input)
    else:
        # Correction
        return correctCases(deaccented_input, word)


def main():
    # Initialization

    # Read input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--dsize", help="Dictionary size",type=int, default=500000)
    parser.add_argument("-d", "--dict", help="Dictionary filename",type=str, default="../Resources/HU_dict")
    parser.add_argument('--timer', dest='timer', help="Timer enabled", action='store_true')
                  
    parser.set_defaults(feature=False)
    args = parser.parse_args()

    dictionary_size = args.dsize
    dictionary_filename = args.dict
    timer_enabled = args.timer

    # If timer is enabled, start timer
    if (timer_enabled):
        start = time.time()

    # Build dictionary
    words_dictionary = {}
    common.buildDict(words_dictionary, dictionary_filename, dictionary_size)


    # read every line of the input
    for l in stdin:

        text = l.decode("utf-8")
        text = text.rstrip('\n')  # strip newline from the end of the line

        deaccented_word = deaccent(text)
        accented_word = accent(deaccented_word, words_dictionary)

        print (accented_word)


    # End
    # Print timer info
    if (timer_enabled):
        end = time.time()
        print ("Finished in " + str(end-start)+" seconds.")

if __name__ == '__main__':
    main()
