# coding: utf-8
__author__ = 'liza'

import numpy as np
import re
from matplotlib import pyplot as plt
from matplotlib import mlab

sub_symb = re.compile('[\r\n«:;,"\'$()%–0-9]')
vowels = 'уеыаоэяиюё'

def words(sentence):
    return sub_symb.sub('', sentence.lower()).split()

def vowel(string):
    return len([letter for letter in string.lower() if letter in vowels])

with open('corpus1.txt', encoding='utf-8') as f:
    corp1 = f.read()
with open('corpus2.txt', encoding='utf-8') as f:
    corp2 = f.read()

corp1_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp1)
corp2_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp2)

corp1_data = [(len(sub_symb.sub('', sentence.replace(' ', ''))), len(set([letter for letter in sub_symb.sub('', sentence.replace(' ', ''))])),
               vowel(sub_symb.sub('', sentence)),
               np.median([len(word) for word in words(sentence)]),
               np.median([vowel(word) for word in words(sentence)]))
              for sentence in corp1_sentences if len(words(sentence)) > 0]
corp2_data = [(len(sub_symb.sub('', sentence.replace(' ', ''))), len(set([letter for letter in sub_symb.sub('', sentence.replace(' ', ''))])),
               vowel(sub_symb.sub('', sentence)),
               np.median([len(word) for word in words(sentence)]),
               np.median([vowel(word) for word in words(sentence)]))
              for sentence in corp2_sentences if len(words(sentence)) > 0]

corp1_data = np.array(corp1_data)
corp2_data = np.array(corp2_data)
#plt.figure()
#c1, c2 = 0, 3
#plt.plot(corp1_data[:, c1], corp1_data[:, c2], 'og',
#         corp2_data[:, c1], corp2_data[:, c2], 'sb')
#plt.show()

data = np.vstack((corp1_data, corp2_data))
p = mlab.PCA(data)
print(p.Wt)
N = len(corp1_data)
plt.figure()
plt.plot(p.Y[:N, 0], p.Y[:N, 1], 'ob', p.Y[N:, 0], p.Y[N:, 1], 'xr')
plt.show()