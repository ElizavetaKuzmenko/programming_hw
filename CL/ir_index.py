# coding: utf-8
__author__ = 'liza'

from pymystem3 import Mystem
import codecs, os, re

m = Mystem()
fpath = './09'
files = os.listdir(fpath)
indices = range(1, len(files) + 1)
files = dict(zip(files, indices))
#print(files)
trash = [' ', '\n', '&', ]
stopwords = set([w.strip().encode('utf-8') for w in codecs.open('stopwords_ru', 'r', 'utf-8').readlines()])
index = {}


def mystem(text):
    text = text.strip().replace(u'«', '').replace('%', '').replace(u'–', '').replace(u'№', '').replace('+', '').replace(u'»', '')
    lemmas = m.lemmatize(text)
    lemmas = [l.strip() for l in lemmas if l not in trash and not l.isdigit() and len(l.strip()) > 1 and
              l.strip() not in stopwords and '(' not in l and ')' not in l and '.' not in l and ',' not in l]
    return lemmas

corp = open('corpus1.txt', 'w', encoding='utf-8')
for f in files:
    text = re.findall('<TEXT>(.*)</TEXT>', codecs.open(fpath + os.sep + f, 'r', 'utf-8').read(),
                      flags=re.DOTALL)[0].replace('<p>', '').replace('</p>', '')
    lemmas = set(mystem(text))
    for l in lemmas:
        try:
            index[l].append(files[f])
        except:
            index[l] = [files[f]]
    corp.write(text + '\n')
corp.close()

nf = codecs.open('Kuzmenko_inverted_index.tsv', 'w', 'utf-8')
for i in sorted(index):
    line = i + '\t'
    for ind in sorted(index[i]):
        line += str(ind) + ','
    nf.write(line[:-1] + '\n')
nf.close()