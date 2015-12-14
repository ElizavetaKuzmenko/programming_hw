# coding: utf-8
__author__ = 'liza'

# + Take a corpus
# + Lemmatize it (texts made from lemmas) -- or pony
# + set of unique lemmas (or uniq)
# + idf dictionary (log(N/df), where N -- number of documents, df -- number of documents with this lemma)
# + tf-idf dictionary with key is text id + lemma, value -- tf-idf for lemma (tf is a freq of lemma in this document)
# + output 10 pairs lemma-document with highest tf-idf

import os, re
from pymystem3 import Mystem
m = Mystem()
from math import log10

fpath = './09'
tpath = './09/562949992267172'
files = os.listdir(fpath)
punct = '\t\r\n%$.,!?–:;()"\''

def read_corpus():
    texts = []
    for t in files:
        with open(fpath + os.sep + t) as f:
            text = re.findall('<TEXT>(.*)</TEXT>', f.read(), flags=re.DOTALL)[0].replace('<p>', '').replace('</p>', '')
            lemmas = [lemma.replace(' ', '') for lemma in m.lemmatize(text) if not lemma.isdigit() and len(lemma) > 1]
            lemmas = [lemma for lemma in lemmas if lemma not in punct and '(' not in lemma and ')' not in lemma
                      and '.' not in lemma and ',' not in lemma]
            texts.append(lemmas)
    return texts


def find_unique(texts):
    lemma_freq = {}
    unique_lemmas = set()
    for text in texts:
        for lemma in text:
            try:
                lemma_freq[lemma] += 1
            except KeyError:
                lemma_freq[lemma] = 1
    for lemma in sorted(lemma_freq, key=lambda lemma: lemma_freq[lemma]):
        # print(lemma, lemma_freq[lemma])
        if lemma_freq[lemma] == 1:
            unique_lemmas.add(lemma)
        else:
            break
    return unique_lemmas


def tf_idf(texts):
    N = len(texts)
    idf_dict = {}
    for text in texts:
        lemmas = set(text)
        for lemma in lemmas:
            try:
                idf_dict[lemma] += 1
            except KeyError:
                idf_dict[lemma] = 1
    for lemma in idf_dict:
        idf_dict[lemma] = 1 + log10(N/idf_dict[lemma])

    tf_idf_dict = {}
    #for textnum in range(len(texts)):
    with open(tpath, 'r', encoding='utf-8') as f:
        text = re.findall('<TEXT>(.*)</TEXT>', f.read(), flags=re.DOTALL)[0].replace('<p>', '').replace('</p>', '')
        lemmas = [lemma.replace(' ', '') for lemma in m.lemmatize(text) if not lemma.isdigit() and len(lemma) > 1]
        lemmas = [lemma for lemma in lemmas if lemma not in punct and '(' not in lemma and ')' not in lemma
                  and '.' not in lemma and ',' not in lemma]
        tf_dict = {}
        for lemma in lemmas:
            try:
                tf_dict[lemma] += 1
            except KeyError:
                tf_dict[lemma] = 1
        for lemma in tf_dict:
            tf_idf_dict[lemma] = 1 + log10(tf_dict[lemma])*idf_dict[lemma]

    return tf_idf_dict


if __name__ == '__main__':
    print('Lemmatizing...')
    texts = read_corpus()
    print('Compiling frequency dictionary...')
    #unique_lemmas = find_unique(texts)
    #print(len(unique_lemmas), '\n', unique_lemmas)
    tf_idf_dict = tf_idf(texts)
    for lemma_doc in sorted(tf_idf_dict, key=lambda lemma_doc: tf_idf_dict[lemma_doc], reverse=True)[:10]:
        print(lemma_doc, tf_idf_dict[lemma_doc], sep=' - ')