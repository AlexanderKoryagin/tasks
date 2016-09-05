#!/usr/bin/env python

# Finding all possible permutations from provided word and checks it generated
# words exists.

from pprint import pprint
import itertools


eng_words_file = 'wordsEn.txt'

a = 'house'
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

pprint(real_words)
