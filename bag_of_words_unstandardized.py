# @wintere
# Demonstration code, limitations of this approach discussed in documentation
# and on the project StoryMaps page.
import re
import csv
import nltk

# Cambridge ED Copy Text
with open('raw-portrait-1881-copy.txt', encoding='utf-8') as f:
	copy_text = f.read().replace("—", " ")

# Tokenize
tokens_1881 = nltk.word_tokenize(copy_text)
x = nltk.pos_tag(tokens_1881)

# Get unweighted bag of copy text words
ct_words = set()
for token in x:
	# Exclude punctuation, etc.
	if token[1] in ['EX', 'RBR', 'MD', 'PRP', 'RB', 'VBZ', 'WRB', 'PDT', 'POS', 'JJS','FW', 'RP', 'WDT', 'JJ', 'DT',  
	'NN', 'IN', 'WP', 'VBN', 'NNP', 'VBD', 'NNS', 'VBG', 'CC', 
	'PRP$', 'UH', 'RBS', 'NNPS', '$', 'JJR', 'VBP', 'WP$', 'VB']:
		ct_words.add(token[0].lower().strip('.'))

# NYE (Unstandardized against CT)
with open('raw-portrait-1908-nye-no-preface.txt', encoding='utf-8') as f:
	copy_text = f.read().replace("—", " ")

# Tokenize
tokens_1908 = nltk.word_tokenize(copy_text)
y = nltk.pos_tag(tokens_1908)

# Get unweighted bag of NYE words
nye_words = set()
for token in y:
	# Exclude punctuation, etc.
	if token[1] in ['EX', 'RBR', 'MD', 'PRP', 'RB', 'VBZ', 'WRB', 'PDT', 'POS', 'JJS','FW', 'RP', 'WDT', 'JJ', 'DT',  
	'NN', 'IN', 'WP', 'VBN', 'NNP', 'VBD', 'NNS', 'VBG', 'CC', 
	'PRP$', 'UH', 'RBS', 'NNPS', '$', 'JJR', 'VBP', 'WP$', 'VB']:
		nye_words.add(token[0].lower().strip('.'))

# Alphabetized ords introduced in NYE (unstandardized), one word per line
with open('words_added_to_nye.txt', mode='w') as io:
	for item in sorted(list(nye_words - ct_words)):
		io.write(item + '\n')

# Alphabetized removed/excluded from CT (standardized), one word per line
with open('words_removed_from_ct.txt', mode='w') as io:
	for item in sorted(list(ct_words - nye_words)):
		io.write(item + '\n')
