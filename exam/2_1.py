# coding: utf-8

import os
import csv
import pandas as pd

PATH_CSV = './data/tfidf.csv'
PATH_DOC = './data/documents.csv'
PATH_W = './data/keywords.csv'

PATH_FEAT = './data/features.csv'
PATH_PRED = './data/predictions.csv'
PATH_T = './data/target.csv'

def import_csv():
    """
    Import data from a given csv file
    :param path: path to CSV file containing tf-idf values for documents
    :return
    """
    with open(PATH_DOC) as f:
        docs = [line.strip() for line in f.readlines()]
    with open(PATH_W) as f:
        words = [line.strip() for line in f.readlines()]
    with open(PATH_CSV) as f:
        values = [line.strip().split(',') for line in f.readlines()]
    for doc in range(len(docs)):
        tf_idf = [float(value) for value in values[doc]]
        found_words = []
        while len(found_words) != 5:
            max_v = max(tf_idf)
            found_words.append(words[tf_idf.index(max_v)])
            tf_idf.pop(tf_idf.index(max_v))
        print(docs[doc], found_words)

def features_csv():
    with open(PATH_FEAT) as f:
        #print(len(f.readlines()))
        features = [line.strip().split(',') for line in f.readlines()]
        #print(len(features[0]))
    with open(PATH_PRED) as f:
        predictions = [line.strip() for line in f.readlines()]
    with open(PATH_T) as f:
        target = [line.strip() for line in f.readlines()]
    new_features = []
    for pred in range(len(predictions)):
        if predictions[pred] != target[pred]:
            new_features.append([float(x) for x in features[pred]])
    df = pd.DataFrame(new_features)
    df = df.loc[:, (df != 0).any(axis=0)]
    print(df)
    print('Column indices\n', df.columns)

if __name__ == '__main__':
    features_csv()