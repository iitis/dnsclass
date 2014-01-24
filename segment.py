#!/usr/bin/env python
"""
Naive Bayes word splitting based on 2012 English Wikipedia

Code heavily based on the code to accompany the chapter
"Natural Language Corpus Data" from the book "Beautiful Data"
by Segaran and Hammerbacher, 2009. For more information, see
http://norvig.com/ngrams/

Copyright (c) 2008-2009 by Peter Norvig
Copyright (c) 2012 by Pawel Foremski <pjf@iitis.pl>
Copyright (c) 2012 by IITiS PAN Gliwice <http://www.iitis.pl/>

You are free to use this code under the MIT licencse: 
http://www.opensource.org/licenses/mit-license.php
"""

import operator
import wikiwords

def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

################ Word Segmentation (p. 223)
@memo
def segment(text):
    "Return a list of words that is the best segmentation of text."
    if not text: return []
    candidates = ([first]+segment(rem) for first,rem in splits(text))
    return max(candidates, key=Pwords)

def splits(text, L=20):
    "Return a list of all possible (first, rem) pairs, len(first)<=L."
    return [(text[:i+1], text[i+1:]) 
            for i in range(min(len(text), L))]

def Pwords(words): 
    "The Naive Bayes probability of a sequence of words."
    return product(Pw(w) for w in words)

#### Support functions (p. 224)
def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

def avoid_long_words(word):
    "Estimate the probability of an unknown word."
    return 10./(wikiwords.N * 10**len(word))

def Pw(word):
	return wikiwords.freq(word, avoid_long_words)

################ Segment stdin
import sys
import re

def main():
	for line in sys.stdin:
		res = []
		for word in re.split('[^a-z0-9]', line.strip().lower()):
			if len(word) > 4:
				res.extend(segment(word))
			else:
				res.append(word)
		print " ".join(res)

if __name__ == "__main__": main()

