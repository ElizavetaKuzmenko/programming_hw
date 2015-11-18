# coding:utf-8
__author__ = 'liza'

import numpy as np
import re
from matplotlib import pyplot as plt

def words(sent):
    return [len(word) for word in sent.split()]

#a = np.array([1, 2, 3])
#a += np.array([4, 3, 1])
#print(a)
#k = np.zeros((4, 4))
#print(k)
#n = np.ones((2, 3)) * 5
#print(n)
#x = np.array([5, 9, 3, 13, 16])
#m = x.mean()
#print(m)
#print(x**2 - m**2)
#s = (x**2 - m**2).mean()**0.5  # среднее квадратичное отклонение
#print(s, x.std())

with open('anna.txt', encoding='utf-8') as f:
    anna = f.read()
with open('sonets.txt', encoding='utf-8') as f:
    sonets = f.read()

anna_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', anna)
sonet_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', sonets)
anna_sentlens = [len(words(sent)) for sent in anna_sentences if len(words(sent)) > 0]
sonet_sentlens = [len(words(sent)) for sent in sonet_sentences if len(sent) > 0]

anna_data = np.array([[len(words(sent)), np.mean(sent), np.median(sent), np.std(sent)] for sent in anna_sentlens])
sonet_data = np.array([[len(words(sent)), np.mean(sent), np.median(sent), np.std(sent)] for sent in sonet_sentlens])

plt.figure()
plt.plot(anna_data[:, 0], anna_data[:, 1], 'o')
plt.show()


