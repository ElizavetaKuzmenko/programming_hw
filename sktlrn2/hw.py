# coding: utf-8
__author__ = 'liza'

# + 1) Возьмите два массива маленьких текстов, например новости про политику и новости про искуссство.
# (Подсказка: например, новости с newsru.com, если их копипастить, можно разбивать split()'ом по символу ":",
# чтобы получить примерный эквивалент разделения на отдельные новости)
# + 2) Постройте для них морфологический анализ (например, с помощью mystem
# (подсказка: соответственно, разбивать текст на части удобнее после mystem, а не до)
# + 3) Прочитайте массивы как списки текстов
# + 4) В каждом тексте постройте число вхождений каждой части речи
# + 5) Постройте таблицу, в которой для каждого предложения для каждой части речи указано количество находок
# этой части речи в этом предложении
# + 6) Присоедините к таблице таблицу векторов tf-idf для этих текстов
# + 7) Создайте массив длины, равной суммарной длине таблиц, содержащий номер коллекции.
# (Это будет значение Y для машинного обучения). (подсказка: штука в духе [0]*len(table1) + [1]*len(table2) делает то, что нужно)
# + 8) Отправьте данные на вход grid_search.GridSearchCV(svm.SVC(), {}) и
# grid_search.GridSearchCV(naive_bayes.MultinomialNB(), {})
# + 9) Покажите процент успеха (best_score_)
# 10) Возьмите наилучший из получившихся классификаторов (best_estimator_), и с его помощью найдите 3 примера,
# где машина угадывает, и 3 примера, где машина ошибается

import re, os, scipy.sparse
import numpy as np
from sklearn import grid_search, svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from pymystem3 import Mystem
m = Mystem()

path_corp1 = './anekdots'
path_corp2 = './izvest'

def mystem(text):
    return m.analyze(text)

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

def prepositions(analysis):
    try:
        return len([w for w in analysis if 'PR=' in w['analysis'][0]['gr']])
    except:
        return 0

def make_pos_table(corp):
    corp_data = []
    for text in corp:
        ana = mystem(text)
        ana = [analysis for analysis in ana if 'analysis' in analysis.keys() and analysis['analysis'] != []]
        corp_data.append([adjectives(ana), nouns(ana), verbs(ana), adverbs(ana), pronouns(ana), prepositions(ana)])
    return corp_data

def make_tfidf_table(corp):
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    X_train_counts = count_vect.fit_transform(corp)
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    return X_train_tfidf

def make_lists(corp_path):
    corp_files = os.listdir(corp_path)
    corp = []
    for f in corp_files:
        with open(corp_path + os.sep + f, 'r', encoding='utf-8') as fi:
            text = fi.read()
            corp.append(text)
    return corp

def classify(data, Y):
    parameters1 = {'C': (.1, .5, 1.0, 1.5, 1.7, 2.0)}
    gs1 = grid_search.GridSearchCV(svm.LinearSVC(), parameters1)
    gs1.fit(data, Y)
    parameters2 = {'alpha': (1e-2, 1e-3)}
    gs2 = grid_search.GridSearchCV(MultinomialNB(), parameters2)
    gs2.fit(data, Y)
    return gs1, gs2

#def find_mistakes(gs, data, Y):
#    clf = gs.best_estimator_
#    clf.fit(data[::2, :], Y[::2])
#    data = scipy.sparse.hstack((Y, data))
#    right = 0
#    wrong = 0
#    for obj in data[1::2, :]:
#        label = clf.predict(obj[1:])
#        if label != obj[0] and wrong < 3:
#            print('Пример ошибки машины: class = ', obj[0], ', label = ', label, ', экземпляр ', obj[1])
#            wrong += 1
#        elif label == Y[obj] and right < 3:
#            print('Пример правильного ответа машины: class = ', obj[0], ', label = ', label, ', экземпляр ', obj[1])
#            right += 1
#        elif right > 3 and wrong > 3:
#            break


if __name__ == '__main__':
    corp1 = make_lists(path_corp1)
    corp2 = make_lists(path_corp2)
    print('Making POS...')
    pos_data = make_pos_table(corp1 + corp2)
    print('Counting tf-idf...')
    tfidf_data = make_tfidf_table(corp1 + corp2)
    data = scipy.sparse.hstack((pos_data, tfidf_data))
    Y = [0]*len(corp1) + [1]*len(corp2)
    print('Classifying...')
    svm, nb = classify(data, Y)
    print('Best result for SVM is ', svm.best_score_)
    print('Best result for NB is ', svm.best_score_)
    #print('Ошибки в SVM:')
    #find_mistakes(svm, data, Y)
    #print('Ошибки в NB:')
    #find_mistakes(nb, data, Y)



