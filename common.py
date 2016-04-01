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

            possible_solutions = []

            if (part in nDict):
                possible_solutions= nDict[part]

            value=0.0
            ngram = ""
            # Find the most frequent N-gram
            for item in possible_solutions:
                if (float(value)<float(item[1])):
                    value=item[1]
                    ngram = item[0].decode("utf-8")

            if (ngram != ""):
                #print ('ngram: '+ngram + ', ' + ngram[diff])
                # Accent the character
                if (character.upper() == character):
                    # It was an upper case character
                    outputWord+= unicode(ngram[nDiff].upper())
                else:
                    # It was a lower case character
                    outputWord+= unicode(ngram[nDiff])
            else:
                outputWord += character

        else:
            outputWord += character
        iterator+=1

    #remove paddings
    #outputWord = outputWord.encode("utf-8").translate(None, ' ').decode("utf-8")
    outputWord = outputWord.strip()
    return outputWord;

