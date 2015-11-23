# coding: utf-8
__author__ = 'liza'

import re
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import mlab
from pymystem3 import Mystem
m = Mystem()
sub_symb = re.compile('[\r\n«:;,"\'$()%–0-9]')

from genre_by_letters import words, vowel, lenwords
from genre_by_pos import nouns, pronouns, adjectives, verbs, adverbs, mystem

def pos_data(sentence):
    ana = mystem(sentence)
    ana = [analysis for analysis in ana if 'analysis' in analysis.keys() and analysis['analysis'] != []]
    return [adjectives(ana), nouns(ana), verbs(ana), adverbs(ana), pronouns(ana)]

def len_data(sentence):
    w = lenwords(sentence)
    if len(w) > 0:
        return [len(w), np.mean(w), np.median(w), np.std(w)]
    else:
        return [0, 0, 0, 0]

def letters_data(sentence):
    l = words(sentence)
    if len(l) > 0:
        return [len(sub_symb.sub('', sent.replace(' ', ''))),
                len(set([letter for letter in sub_symb.sub('', sent.replace(' ', ''))])),
                vowel(sub_symb.sub('', sent)),
                np.median([len(word) for word in l]),
                np.median([vowel(word) for word in l])]
    else:
        return [0, 0, 0, 0, 0]

with open('anna.txt', encoding='utf-8') as f:
    corp1 = f.read()
with open('sonets.txt', encoding='utf-8') as f:
    corp2 = f.read()
with open('news.txt', encoding='utf-8') as f:
    corp3 = f.read()

corp1_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp1)
corp2_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp2)
corp3_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp3)

corp1_data = []
corp2_data = []
corp3_data = []

print('Processing corpus1...')
for sent in corp1_sentences:
    corp1_data.append(pos_data(sent) + len_data(sent) + letters_data(sent))

print('Processing corpus2...')
for sent in corp2_sentences:
    corp2_data.append(pos_data(sent) + len_data(sent) + letters_data(sent))

print('Processing corpus3...')
for sent in corp3_sentences:
    corp3_data.append(pos_data(sent) + len_data(sent) + letters_data(sent))

corp1_data = np.array(corp1_data)
corp2_data = np.array(corp2_data)
data = np.vstack((corp1_data, corp2_data))
p = mlab.PCA(data)
print(p.Wt)
N = len(corp1_data)
plt.figure()
plt.plot(p.Y[:N, 0], p.Y[:N, 1], 'ob', p.Y[N:, 0], p.Y[N:, 1], 'xr')
plt.show()