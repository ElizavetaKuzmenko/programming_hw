# coding: utf-8
__author__ = 'liza'


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import mlab
import re, time
from pymystem3 import Mystem
m = Mystem()

def mystem(sentence):
    sentence = sentence.strip()
    anas = m.analyze(sentence)
    return anas

def nouns(analysis):
    try:
        return len([w for w in analysis if 'S,' in w['analysis'][0]['gr']])
    except:
        return 0

def adjectives(analysis):
    try:
        return len([w for w in analysis if 'A=' in w['analysis'][0]['gr']])
    except:
        return 0

def verbs(analysis):
    try:
        return len([w for w in analysis if 'V,' in w['analysis'][0]['gr']])
    except:
        return 0

def adverbs(analysis):
    try:
        return len([w for w in analysis if 'ADV=' in w['analysis'][0]['gr']])
    except:
        return 0

def pronouns(analysis):
    try:
        return len([w for w in analysis if 'PRO' in w['analysis'][0]['gr']])
    except:
        return 0

if __name__ == '__main__':
    print('Reading', time.asctime())
    with open('anna.txt', encoding='utf-8') as f:
        corp1 = f.read()
    with open('sonets.txt', encoding='utf-8') as f:
        corp2 = f.read()

    corp1_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp1)
    corp2_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp2)
    corp1_data = []
    corp2_data = []

    print('Analyzing corpus1', time.asctime())
    for sent in corp1_sentences:
        ana = mystem(sent)
        ana = [analysis for analysis in ana if 'analysis' in analysis.keys() and analysis['analysis'] != []]
        corp1_data.append([adjectives(ana), nouns(ana), verbs(ana), adverbs(ana), pronouns(ana)])

    print('Analyzing corpus2', time.asctime())
    for sent in corp2_sentences:
        ana = mystem(sent)
        ana = [analysis for analysis in ana if 'analysis' in analysis.keys() and analysis['analysis'] != []]
        corp2_data.append([adjectives(ana), nouns(ana), verbs(ana), adverbs(ana), pronouns(ana)])

    print('Checking', time.asctime())
    for arr in corp1_data:
        print(arr)
    for arr in corp2_data:
        print(arr)

    print('PCA and drawing', time.asctime())
    corp1_data = np.array(corp1_data)
    corp2_data = np.array(corp2_data)
    data = np.vstack((corp1_data, corp2_data))
    p = mlab.PCA(data)
    print(p.Wt)
    N = len(corp1_data)
    plt.figure()
    plt.plot(p.Y[:N, 0], p.Y[:N, 1], 'ob', p.Y[N:, 0], p.Y[N:, 1], 'xr')
    plt.show()