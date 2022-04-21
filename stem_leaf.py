# @wintere

# Inspired by Richard Brath's JSON textual stem and leaf plot
# available at https://observablehq.com/@abebrath/word-associations-stem-and-leaf
from collections import defaultdict
import re
import nltk
import pandas
import csv

# Stubborn contraction fragments from the default tokenizer
ADDITIONAL_STOPWORDS = ['n\'t', ',', '.', '!', '?', '\'s', 'could', 'would','may', 'put', 'one', 'us',
'should',';', 've', '\'d', '\'re', ':', '\'m', 'le', '\'\'', '\'ve', '\'ll', '``', ')', '(','wo','ca']

def main(csv_f):
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords.extend(ADDITIONAL_STOPWORDS)
	replacements = defaultdict(int)
	grouped_replacements = {}
	# read in the cleaned CSV data in utf-8 format because James likes his française
	# unicode is required to support accented characters
	df = pandas.read_csv(csv_f, encoding='utf-8', 
		encoding_errors='strict', na_filter=False)
	# iterate through each row (change) in the data frame
	# Initialize lemmatizer
	lemmatizer = nltk.wordnet.WordNetLemmatizer()
	for index, row in df.iterrows():
		# chapter, page, before, after
		c, p, b, a = row['chapter'], row['page'], row['cam_1882'], row['cam_NYE']

		# clean out characters that don't tokenize cleanly
		b, a = b.replace("—", " "), a.replace("—", " ")

		# tokenize and tag
		b_tokens = set(nltk.pos_tag(nltk.word_tokenize(b), tagset='universal'))
		a_tokens = set(nltk.pos_tag(nltk.word_tokenize(a), tagset='universal'))

		# construct replacement pair objects (b, a, #count replacement is made)
		# the words unique to before (b) are b - (instersection of b and after a)
		b_unique = set(b_tokens) - b_tokens.intersection(a_tokens)
		a_unique = set(a_tokens) - a_tokens.intersection(b_tokens)
		for orig in b_unique:
			if orig[0].lower() not in stopwords and orig[1] not in ['X','PRON']:		
				before = lemmatizer.lemmatize(orig[0].lower())
			else:
				continue
			for repl in a_unique:
				if repl[0].lower() not in stopwords and repl[1] not in ['X','PRON']:
					if repl[0] == 'DELETION': 		#skip deletions
						continue
					after = lemmatizer.lemmatize(repl[0].lower())
					if before != after:
						replacements[(before, after)] += 1
						if before not in grouped_replacements:
							grouped_replacements[before] = {}
							grouped_replacements[before][after] = 1
						else:
							if after in grouped_replacements[before]:
								grouped_replacements[before][after] += 1
							else:
								grouped_replacements[before][after] = 1

	# Order and emit replacement patterns, grouped by original by frequency
	with open('words_to_revisions.csv', 'w', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Word In 1882", "Words in Replacement Lines"])
		for replaced in sorted(grouped_replacements.keys()): # emit results in ABC order
			# Fetch replacements from dictionary, order by freq of replacement
			repl = grouped_replacements[replaced]
			repl_list = sorted(repl.items(), key=lambda item: item[1], reverse=True)
			tab_sep_repl = ','.join([item[0] for item in repl_list])
			writer.writerow([replaced, tab_sep_repl])

	# Also, write out the most common one to one replacements
	with open('words_to_revisions_freq.csv', 'w', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Word In 1882 Line", "Words in Replacement Line", "Frequency"])
		# Order by frequency
		ordered_r = sorted(replacements.items(), key=lambda item: item[1], reverse=True)
		for item in ordered_r:
			writer.writerow([item[0][0], item[0][1], item[1]])


if __name__ == '__main__':
	main("cleaned_output.csv")