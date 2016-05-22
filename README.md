Diacritic Restoration
===================

#### Version
1.0

#### Dictionary-based method
##### Parameters
* -d or --dict sets the source dictionary file, with a default value of “../Resources/HU\_dict”
* -s or --dsize sets the dictionary size (how many words are going to be used by the script), with a default value of 500,000 words
* --timer flag, if present, enables the script to measure and print its own processing time

>cat input_file | python accent_dict.py -d ../Resources/Custom_dict -s 2000000 --timer


#### N-gram method
##### Parameters
* -d or --dict sets the source dictionary file, with a default value of “../Resources/HU\_2gram\_dict”
* -n or --ngram sets the $N$ value of the \mbox{N-gram} method, with a default value of 2
* -a or --accents sets the accents mapping for the given language, with a default value of \emph{áaéeíióoöoőoúuüuűu}, which is the correct accent mapping for Hungarian language. The map consist of character pairs, the first one is the accented form, the second one is the ASCII form of the character without diacritics
* --timer flag, if present, enables the script to measure and print its own processing time

>cat input_file  | python accent_ngram.py -d ../Resources/Custom_5gram_dict -n 2 --accents %*äaáaàaèaée*)


#### Combined method
##### Parameters
* -d or --dict sets the source dictionary file, with a default value of “../Resources/HU\_dict”
* -s or --dsize sets the dictionary size (how many words are going to be used by the script), with a default value of 500,000 words,
* --ngram$ flag, if present, enables the \mbox{N-gram} method, therefore the combination of the two methods too, by default this is disabled
* -n sets the N value of the \mbox{N-gram} method, with a default value of 2
* -ndict or --ndict sets the source dictionary file for the \mbox{N-gram} method, with a default value of “../Resources/HU\_2gram\_dict”
* -nsize or --nsize sets the \mbox{N-gram} dictionary size, by default, it's value is the length of the default dictionary
* -a or --accents sets the accents mapping for the given language, with a default value of \emph{áaéeíióoöoőoúuüuűu}, which is the correct accent mapping for Hungarian language. The map consist of character pairs, the first one is the accented form, the second one is the ASCII form of the character without diacritics
* --timer flag, if present, enables the script to measure and print its own processing time

>cat input_file  | python accent_combined.py -d ../Resources/Custom_dict -s 2000000 --ngram -n 2 -nsize 500000  --accents %*äaáaàaèaée*) --timer



### License
MIT.
