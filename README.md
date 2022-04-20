# portrait-vis
The intermediate outputs and visualization code for a final project for ENGLISH 590: Quantifying Literature.  

Because Henry James's *The Portrait of a Lady* is in the public domain the only file I have omitted from this repository is the PDF list of textual variants from [this edition of the book](https://www.cambridge.org/core/books/abs/portrait-of-a-lady/textual-variants/043E375660B293FE913A585215206122) because the changelist is supplemented with editorial material under copyright. I extracted the variants from the PDF chapter and converted them to a text file cambridge-textual-variants.txt.

## Data Cleaning

*Data cleaning that can consume infinite time.*

## The Bag of Words Model

I wanted to start with the lowest hanging fruit: independent of grammatical nuance and ordering, did the revision process introduce and remove words from *The Portrait of a Lady*? Prior criticism says yes, words were introduced (like "Schubert" and "perversity") and words were removed ("picturesque" for its vagueness"), but how do those introductions and removals look at scale?

This can be determine using word tokenization and a little set theory.

![image](https://user-images.githubusercontent.com/7553742/164237906-c96992b1-208c-415b-b182-489b970961b3.png)

For any two intersecting sets A and B, the items unique to A are A - (A & B). That is, the items unique to A are all items in A with all the items in both A and B removed.

Because the two versions of *The Portrait*, the New York Edition (NYE) and 1882 copy-text (CT) are near identical in dialogue, structure, and incident, the overlapping sets will like more like this:

![image](https://user-images.githubusercontent.com/7553742/164240328-5287033b-cb63-4064-906f-64d79947b1fb.png)

### Attempt #1: processing changes on the word level, no context

bag_of_words_unstandardized.py

Usage: 
```
python3 bag_of_words_unstandardized.py
```

## Attempt #2: processing changes on the word level, contextualized *within* a change


Usage: 
```
python3 bag_of_words_unstandardized.py
```
