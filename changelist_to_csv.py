# @wintere
import re
import csv


# Open the variants extracted from Cambridge Edition PDF (not included)
# Expects variants in the form Page#.Line# before]after
with open('cambridge-textual-variants.txt', encoding='utf-8') as f:
	data = f.read()

# Organizes changes by chapter, page (1882), and first line (1882)
chapter_splits = re.split(r'CHAPTER[\d]+', data)
changes_header = ["chapter", "page", "line", "1882", "1908", "change_type"]
c = 
with open('out.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
	writer.writerow(changes_header)
	for chapter in chapter_splits:
		tuples = re.findall(r'([\d]+\.[\d]+) ([^\d]+)', chapter)
		# extract page and line number
		for tup in tuples:
			p, l = tup[0].split('.')
			# Separate before from after
			edits = tup[1].replace('\n', ' ').split(']')
			if len(edits) == 2: #All changes need a before + after
				change_type = ""
				if edits[1].strip() == "DELETION":
					change_type="deletion"
				row = [c, p, l, edits[0].strip(), edits[1].strip(), change_type]
				writer.writerow(row)
			else:
				print("Unable to process change line: ")
				print(edits)
		c += 1
