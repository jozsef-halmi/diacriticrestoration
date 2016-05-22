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

def deaccent( word ):
    return common.remove_accents(unicode(word))

def sortTupleArray ( array, index ):
    array.sort(key=operator.itemgetter(index))
    return array;


def findCandidates ( inputWord, words_dictionary):
    list = []
    if (inputWord in words_dictionary):
        list = words_dictionary[inputWord]

    return list;

def findMostFrequent ( inputWord, words_dictionary ):
    if (inputWord in words_dictionary):
        return words_dictionary[inputWord];

    return "";

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

def accent(deaccented_input, words_dictionary, ngram_enabled, ngram_dict, ngram_diff, ngram_accents, ngram_prevString, ngram_follString):
    istitle = (deaccented_input.istitle())
    word = findMostFrequent(deaccented_input.lower(),words_dictionary)
    if (word == ""):
        # No correction, copy (OOV)
        # N-gram
        if (ngram_enabled):
            ngram_result=common.ngramAccent ( deaccented_input, ngram_dict, ngram_diff,
                                              ngram_accents,  ngram_prevString, ngram_follString,
                                              common.getPaddingChar() )
            #ngram_result = ngram_accent( deaccented_input, ngram_dict, ngram_diff,
            #                             ngram_accents, ngram_prevString, ngram_follString)
            return correctCases(deaccented_input, ngram_result)

        return (deaccented_input)
    else:
        # Correction
        return correctCases(deaccented_input, word)


def accentWithNgram(buffer, N, ngram_diff, words_dictionary,accents, ngram_dict, padding_char, text):
    deaccented_word = deaccent(text)
    buffer.pop(0)
    buffer.append(deaccented_word)

    prevText = padding_char.join(buffer[0:ngram_diff])
    follText = padding_char.join(buffer[ngram_diff+1:N])
    word = buffer[ngram_diff]
    accented_word = accent(word, words_dictionary,
                           True, ngram_dict, ngram_diff, accents,
                           prevText, follText)
    return accented_word



def main():
    # Initialization

    # Read input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--dsize", help="Dictionary size",type=int, default=500000)
    parser.add_argument("-d", "--dict", help="Dictionary filename",type=str, default="../Resources/HU_dict")
    parser.add_argument('--ngram', dest='ngram_enabled', help="NGram enabled", action='store_true')
    parser.add_argument("-n", "--n", help="N value for N-gram, such as 1,2,3,4,5..",type=int, default=2)
    parser.add_argument("-ndict", "--ndict", help="Ngram dictionary file",type=str, default="Resources/HU_2gram_dict")
    parser.add_argument("-nsize", "--nsize", help="Ngram dictionary size",type=int, default=1133518)
    parser.add_argument('--timer', dest='timer', help="Timer enabled", action='store_true')
    parser.add_argument('--accents', type=str, default='áaéeíióoöoőoúuüuűu',
                   help='accent mapping')
    parser.set_defaults(feature=False)
    args = parser.parse_args()

    dictionary_size = args.dsize
    dictionary_filename = args.dict


    timer_enabled = args.timer
    ngram_enabled = args.ngram_enabled
    accents = args.accents
    # N-gram parameter

    ngram_diff = args.n
    N = (2*ngram_diff)+1
    ngram_dictname = args.ndict
    ngram_dictsize = args.nsize
    # If timer is enabled, start timer
    if (timer_enabled):
        start = time.time()

    

    words_dictionary = {}
    ngram_dict = {}
    common.buildDict(words_dictionary, dictionary_filename, dictionary_size)
    
    if (ngram_enabled == True):
        common.buildDict(ngram_dict, ngram_dictname, ngram_dictsize)

    padding_char = common.getPaddingChar()

    word_buffer = []
    for i in range(0,N):
        word_buffer.append("")

    initCounter = 0

    # read every line of the input
    for l in stdin:

        text = l.decode("utf-8")
        text = text.rstrip('\n')  # strip newline from the end of the line

        if (ngram_enabled == False):
            deaccented_word = deaccent(text)
            accented_word = accent(deaccented_word, words_dictionary, ngram_enabled, ngram_dict, ngram_diff, accents, "","")
            print (accented_word)
        else:
            if (initCounter < ngram_diff):
                initCounter += initCounter + 1
                word_buffer.pop(0)
                word_buffer.append(text)

            else:
                accented_word = accentWithNgram(word_buffer, N, ngram_diff, words_dictionary, accents, ngram_dict,
                                                padding_char, text)
                print (accented_word)



    # Last ngram_diff iterations
    for i in range(0,ngram_diff):
        accented_word = accentWithNgram(word_buffer, N, ngram_diff, words_dictionary, accents, ngram_dict,
                                                padding_char, "")
        print (accented_word)

    # End
    # Print timer info
    if (timer_enabled):
        end = time.time()
        print ("Finished in " + str(end-start)+" seconds.")

if __name__ == '__main__':
    main()
