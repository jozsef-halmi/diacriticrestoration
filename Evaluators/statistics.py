#-*- coding: utf-8 -*-
from sys import stdin
import re
import argparse
from collections import defaultdict
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def deaccent( word ):
    return remove_accents(unicode(word))

def convert_mapping(str_map):
    mapping = {}
    map_u = str_map.decode('utf8')
    mapping = {
            map_u[i]: map_u[i + 1] for i in xrange(0, len(map_u), 2)
    }
    return mapping

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--accents', type=str, default='áaéeíióoöoőoúuüuűu',
                   help='accent mapping')
    args = parser.parse_args()

    # Variables for vowels
    FALSE_POSITIVE = 0
    TRUE_POSITIVE = 0
    FALSE_NEGATIVE = 0
    TRUE_NEGATIVE = 0

    # Variables for word-level statistics
    WFALSE_POSITIVE = 0
    WTRUE_POSITIVE = 0
    WFALSE_NEGATIVE = 0
    WTRUE_NEGATIVE = 0

    # Statistics for letters
    LGOOD = 0
    LBAD = 0

    accent_map = convert_mapping(args.accents)
    accent_set = set(accent_map.iterkeys())


    # for individual statistics
    counter = defaultdict(int)


    for l in stdin:  # every line in the input
        text = l.decode('utf8')  # decode from utf-8 encoded string
        text = text.rstrip('\n')  # strip newline from the end of the line
        words = text.split("\t")
        if (len(words)>1 and len(words[0]) == len(words[1])):

            # Word level statistics
            if (words[0] == words[1]):

                # Output is correct
                if(set(words[1]) & accent_set):
                    WTRUE_POSITIVE += 1
                else:
                    WTRUE_NEGATIVE +=1
            else:
                 # Output is not correct
                 if(set(words[1]) & accent_set):
                     WFALSE_NEGATIVE += 1
                 else:
                     WFALSE_POSITIVE +=1

            # Letter level statistics
            for index, input_character in enumerate(words[0]):
                suggested_character = words[1][index]

                # Input and suggested character equals
                if (input_character == suggested_character):
                    LGOOD += 1

                    # if character is an accent char either in deaccented or accented form
                    if (input_character in args.accents.decode('utf-8')):

                        # Accent statistics
                        if (suggested_character in accent_map):
                            TRUE_POSITIVE += 1

                            # individual accent statistics
                            # tp stands for true positive
                            counter[deaccent(input_character)+'tp'] +=1
                            #print ("TP "+ input_character + " "+suggested_character)
                        else:
                            TRUE_NEGATIVE += 1

                            # individual accent statistics
                            # tp stands for true negative
                            counter[deaccent(input_character)+'tn'] +=1
                else:
                    LBAD += 1

                    # if character is an accent char either in deaccented or accented form
                    if (input_character in args.accents.decode('utf-8')):
                        # Accent statistics
                        if (suggested_character not in accent_map):
                            FALSE_NEGATIVE += 1

                            # individual accent statistics
                            # tp stands for false negative
                            counter[deaccent(input_character)+'fn'] +=1
                        else:
                            FALSE_POSITIVE += 1
                            # individual accent statisticskey_character
                            # tp stands for false positive
                            counter[deaccent(input_character)+'fp'] +=1
                            #print ("FP "+ input_character + " "+suggested_character)

    print ("Printing word-level statistics. ")
    # Calculate Precision, Recall, Accuracy, FScore for words
    w_precision = (WTRUE_POSITIVE/float(WTRUE_POSITIVE+WFALSE_POSITIVE))
    print("Precision: "+str(w_precision))
    w_recall = (WTRUE_POSITIVE/float(WTRUE_POSITIVE+WFALSE_NEGATIVE))
    print("Recall: "+str(w_recall))
    w_accuracy = (WTRUE_POSITIVE+WTRUE_NEGATIVE)/float(WTRUE_POSITIVE+WTRUE_NEGATIVE+WFALSE_NEGATIVE+WFALSE_POSITIVE)
    print("Accuracy: "+str(w_accuracy))
    w_fscore = (2*w_precision*w_recall)/float(w_precision+w_recall)
    print("F-Score: "+str(w_fscore))
    # Print out the statistics for words
    #print ("WTP{0}\tWTN{1}\tWFP{2}\tWFN{3}\tP{4}\tR{5}\tA{6}\tF{7}".format(WTRUE_POSITIVE,WTRUE_NEGATIVE,WFALSE_POSITIVE,WFALSE_NEGATIVE,
    #                                                       w_precision,w_recall,w_accuracy,w_fscore))

    print("")
    print("")
    print ("Printing grapheme-level statistics. ")

    # Calculate Precision, Recall, Accuracy, FScore for accents
    a_precision = (TRUE_POSITIVE/float(TRUE_POSITIVE+FALSE_POSITIVE))
    print("Precision: "+str(a_precision))
    a_recall = (TRUE_POSITIVE/float(TRUE_POSITIVE+FALSE_NEGATIVE))
    print("Recall: "+str(a_recall))
    a_accuracy = (TRUE_POSITIVE+TRUE_NEGATIVE)/float(TRUE_POSITIVE+TRUE_NEGATIVE+FALSE_NEGATIVE+FALSE_POSITIVE)
    print("Accuracy: "+str(a_accuracy))
    a_fscore = (2*w_precision*w_recall)/float(w_precision+w_recall)
    print("F-Score: "+str(a_fscore))


    # Print out the statistics for accents
    #print ("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(TRUE_POSITIVE,TRUE_NEGATIVE,FALSE_POSITIVE,FALSE_NEGATIVE,
    #                                                       a_precision,a_recall,a_accuracy,a_fscore))

    print("")
    print("")
    print("Character-level statistics.")
    # Calculate Accuracy for letters
    l_accuracy = LGOOD / (LGOOD+LBAD)
    #print ("{0}\t{1}\t{2}".format(LGOOD,LBAD,l_accuracy))


    # individual accent statistics
    for character, stat in sorted(counter.iteritems(),
                                   key=lambda x: x[0]):
        print ("{0}\t{1}".format(character.encode('utf-8'),stat))


# if the script is called directly (as opposed to being imported)
# call the main function.
# This prevents it from being run when this module is imported
if __name__ == '__main__':
    main()
