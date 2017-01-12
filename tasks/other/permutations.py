#!/usr/bin/env python
"""Find all possible permutations from provided word.

And checks if generated words exists.
"""


import itertools
from pprint import pprint
import sys


eng_words_file = 'wordsEn.txt'

a = sys.argv[1:][0] if len(sys.argv[1:]) > 0 else 'house'
a = list(a)

with open(eng_words_file, 'r') as f:
    words_list = [line.strip() for line in f]

real_words = []
for i in range(1, len(a) + 1):
    combinations = list(itertools.permutations(a, i))

    for variant in combinations:
        word = ''.join(variant)
        if word in words_list and word not in real_words:
            real_words.append(word)

pprint(list(enumerate(real_words, start=1)))
