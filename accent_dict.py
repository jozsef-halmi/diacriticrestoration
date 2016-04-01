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

# Builds up the dictionary used in diacritic restoration 
def buildDict (words_dictionary, dictionary_filename, dictionary_size):
    with open(dictionary_filename) as dict:
        head = [next(dict) for x in xrange(dictionary_size)]

        for line in head:
            words = line.decode("utf-8").split("\t")

            actualWord = common.remove_accents(unicode(words[0]).lower())
            if (not actualWord in words_dictionary):
                words_dictionary[actualWord] = [(words[0], words[1])]
            else:
                words_dictionary[actualWord].append((words[0], words[1]))


# Returns the candidates for a given word
def findCandidates ( inputWord, words_dictionary):
    list = []
    if (inputWord in words_dictionary):
        list = words_dictionary[inputWord]

    return list;

# Finds the most frequent word from the candidates and returns it
def findMostFrequent ( inputWord, words_dictionary ):
    list = []
    if (inputWord in words_dictionary):
        list = words_dictionary[inputWord]
    value=0.0
    word = ""

    for item in list:
        if (float(value)<float(item[1])):
            value=item[1]
            word = item[0]

    return word;

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
    word = findMostFrequent(deaccented_input.lower(),words_dictionary)
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
    parser.add_argument('-a', "--adv", action='store_true',  help="Collect advanced statistics. Input needs to be diacreted!")
    parser.add_argument('--timer', dest='timer', help="Timer enabled", action='store_true')
                  
    parser.set_defaults(feature=False)
    args = parser.parse_args()

    dictionary_size = args.dsize
    dictionary_filename = args.dict
    timer_enabled = args.timer
    advanced_stat = args.adv

    # If timer is enabled, start timer
    if (timer_enabled):
        start = time.time()

    if (advanced_stat):
        #Advanced stats
        OOV_COUNT = 0
        BAD_DIACRITICS_COUNT = 0
        GOOD_DIACRITICS_COUNT = 0

    # Build dictionary
    words_dictionary = {}
    buildDict(words_dictionary, dictionary_filename, dictionary_size)


    # read every line of the input
    for l in stdin:

        text = l.decode("utf-8")
        text = text.rstrip('\n')  # strip newline from the end of the line

        deaccented_word = deaccent(text)
        accented_word = accent(deaccented_word, words_dictionary)
        if (advanced_stat):
            candidates = findCandidates(deaccented_word, words_dictionary)
            if (text == accented_word):
                GOOD_DIACRITICS_COUNT += 1
            else:
                candidates = findCandidates(deaccented_word, words_dictionary)
                candidatesText = ','.join([str(i[0]) for i in candidates])
                if (text in candidatesText):
                    BAD_DIACRITICS_COUNT +=1
                    print (text + "\t"+accented_word + "\t" + "BAD")
                else:
                    OOV_COUNT +=1
                    print (text + "\t"+accented_word + "\t" + "OOV")
                print (candidatesText)
        else:
            print (accented_word)
       


    # End
    if (advanced_stat):
        print ("OOV Count: "+str(OOV_COUNT))
        print ("BAD Count: "+str(BAD_DIACRITICS_COUNT))
        print ("GOOD Count: "+str(GOOD_DIACRITICS_COUNT))
    # Print timer info
    if (timer_enabled):
        end = time.time()
        print ("Finished in " + str(end-start)+" seconds.")

if __name__ == '__main__':
    main()
