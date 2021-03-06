# coding: utf-8
__author__ = 'liza'

import re
import numpy as np
from math import fabs
from matplotlib import pyplot as plt
from matplotlib import mlab
from pymystem3 import Mystem
m = Mystem()
sub_symb = re.compile('[\r\n«:;,"\'$()%–0-9]')
features = {1: 'number of adjectives', 2: 'number of nouns', 3: 'number of verbs', 4: 'number of adverbs',
            5: 'number of pronouns', 6: 'lenght of sentence in words', 7: 'mean lenght of word',
            8: 'median length of word', 9: 'std of length of word', 10: 'length of word in symbols',
            11: 'number of different symbols in sentence', 12: 'number of vowels in sentence',
            13: 'median length of word', 14: 'median number of vowels in a word'}

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
corp3_data = np.array(corp3_data)
data = np.vstack((corp1_data, corp2_data, corp3_data))
N = len(corp1_data)
L = len(corp3_data)
p = mlab.PCA(data)
print(p.mu, p.Wt)
plt.figure()
plt.plot(p.Y[:N, 0], p.Y[:N, 1], 'xb', p.Y[N:L, 0], p.Y[N:L, 1], 'xr', p.Y[L:, 0], p.Y[L:, 1], 'xg')
plt.savefig('SVD.png', bbox_inches='tight')
print('The most informational features:')
inf_features = []
max_useful = sorted([fabs(x) for x in p.Wt[:, 0]])[:3]
for x in range(len(p.Wt[:, 0])):
    if fabs(p.Wt[:, 0][x]) in max_useful:
        print(features[x + 1], p.Wt[:, 0][x])
        inf_features.append(x)
for feature1 in inf_features:
    for feature2 in inf_features:
        if feature1 != feature2 and feature1 < feature2:
            plt.figure()
            plt.plot(corp1_data[:, feature1], corp1_data[:, feature2], 'xr', corp2_data[:, feature1],
                     corp2_data[:, feature2], 'xb', corp3_data[:, feature1], corp3_data[:, feature2], 'xg')
            plt.savefig('feature%s_vs_feature%s.png' % (feature1 + 1, feature2 + 1), bbox_inches='tight')