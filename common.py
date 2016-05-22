import unicodedata
import logging
logging.basicConfig(filename='accent.log',level=logging.INFO)

def logInfo(text):
    logging.info(text)


def logError(text):
    logging.error(text)


def replace(text):
    for ch in ['\\', ',', '"', '\'', '?',';',':','`','*','_','{','}','[',']','(',')','>','<','#','+','-','.','!','$','\'']:
        text = text.replace(ch," ")

    return text

# Removes accents from a string
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])



def getPaddingChar():
    return ' '


    
def ngramAccent ( inputWord, nDict, nDiff, accents,  nPrevStr, nFollStr, paddingChar ):
    outputWord = ""
    wordStartIndex = len(nPrevStr)
    wordEndIndex = len(nPrevStr) + len(inputWord) + 1


    fullText = nPrevStr + paddingChar + inputWord + paddingChar + nFollStr
    for iterator in range(wordStartIndex, wordEndIndex):
        character = fullText[iterator]

        if (character.lower() in accents):
            temp = fullText[iterator-nDiff:iterator+nDiff+1].lower()

            part = []
            i = 0
            for char in temp:
                if (char.isalpha() == False):
                    part.append(' ')
                else:
                    part.append(char)
                i = i+1

            part = ''.join(part)

            candidate = ""

            if (part in nDict):
                candidate= nDict[part]
                
            if (candidate != ""):
                # Accent the character
                if (character.upper() == character):
                    # It was an upper case character
                    outputWord+= unicode(candidate[nDiff].upper())
                else:
                    # It was a lower case character
                    outputWord+= unicode(candidate[nDiff])
            else:
                outputWord += character

        else:
            outputWord += character
        iterator+=1

    #remove paddings
    #outputWord = outputWord.encode("utf-8").translate(None, ' ').decode("utf-8")
    outputWord = outputWord.strip()
    return outputWord;

# The function returns a boolean value, representing
# whether the input string contains accentable character(s) or not.
def isAccentable( str, accent_string ):
    if any((c in accent_string) for c in str):
        return True
    else:
        return False

# Returns the line count of a file
def fileLineCount(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
    
# Builds up the dictionary used in diacritic restoration 
def buildDict (words_dictionary, dictionary_filename, dictionary_size):

    # If the given dictionary size is larger than the given dictionary size, use that instead
    dictionary_max = fileLineCount(dictionary_filename)
    # Check if given number is not greater than the dictionary real size
    if (dictionary_max<dictionary_size):
        # The real length will be the minimum of the two values
        dictionary_size = dictionary_max

    with open(dictionary_filename) as dict:
        head = [next(dict) for x in xrange(dictionary_size)]

        for line in head:
            words = line.decode("utf-8").split("\t")

            actualWord = remove_accents(unicode(words[0]).lower())
            if (not actualWord in words_dictionary):
                words_dictionary[actualWord] = words[0]
            #else:
            #    words_dictionary[actualWord].append((words[0], words[1]))

    