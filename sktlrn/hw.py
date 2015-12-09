# coding: utf-8
__author__ = 'liza'

# + 1. Возьмите два больших текста, например, "Война и Мир" и "Капитал"
# + 2. Постройте для них морфологический анализ (например, с помощью mystem -d -n -i -s --format=json --eng-gr in.txt out.txt)
# + 3. Прочитайте тексты по предложениям
# + 4. В каждом предложении постройте число вхождений каждой части речи
# + 5. Постройте таблицу, в которой для каждого предложения для каждой части речи указано количество находок этой части речи в этом предложении
# + 6. Присоедините к таблице столбик с номером текста
# + 7. Отправьте данные на вход grid_search.GridSearchCV(svm.SVC(), {...})
# (вместо ... перечислите разные значения C)
# + 8. Покажите процент успеха (best_score_)
# + 9. Возьмите наилучший из получившихся классификаторов (best_estimator_), и с его помощью найдите 3 примера, где машина угадывает, и 3 примера, где машина ошибается

import re
import numpy as np
from sklearn import grid_search, svm
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

def prepositions(analysis):
    try:
        return len([w for w in analysis if 'PR=' in w['analysis'][0]['gr']])
    except:
        return 0

if __name__ == '__main__':
    with open('capital.txt', 'r', encoding='utf-8') as f:
        corp1 = f.read()
    with open('anna.txt', encoding='utf-8') as f:
        corp2 = f.read()

    corp1_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp1)
    corp2_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', corp2)
    corp1_data = []
    corp2_data = []

    print('Processing corp1...')
    for sent in corp1_sentences:
        ana = mystem(sent)
        ana = [analysis for analysis in ana if 'analysis' in analysis.keys() and analysis['analysis'] != []]
        corp1_data.append([1, adjectives(ana), nouns(ana), verbs(ana), adverbs(ana), pronouns(ana), prepositions(ana)])
    print('Processing corp2...')
    for sent in corp2_sentences:
        ana = mystem(sent)
        ana = [analysis for analysis in ana if 'analysis' in analysis.keys() and analysis['analysis'] != []]
        corp2_data.append([2, adjectives(ana), nouns(ana), verbs(ana), adverbs(ana), pronouns(ana), prepositions(ana)])

    corp1_data = np.array(corp1_data)
    corp2_data = np.array(corp2_data)
    data = np.vstack((corp1_data, corp2_data))

    print('Classifying...')
    parameters = {'C': (.1, .5, 1.0, 1.5, 1.7, 2.0)}
    gs = grid_search.GridSearchCV(svm.LinearSVC(), parameters)
    gs.fit(data[:, 1:], data[:, 0])
    print('Best result is ',gs.best_score_)
    clf = svm.LinearSVC(C=gs.best_estimator_.C)
    clf.fit(data[::2, 1:], data[::2, 0])
    right = 0
    wrong = 0
    for obj in data[1::2, :]:
        print(obj)
        label = clf.predict(obj[1:])
        if label != obj[0] and wrong < 3:
            print('Пример ошибки машины: class = ', obj[0], ', label = ', label, ', экземпляр ', obj[1:])
            wrong += 1
        elif label == obj[0] and right < 3:
            print('Пример правильного ответа машины: class = ', obj[0], ', label = ', label, ', экземпляр ', obj[1:])
            right += 1
        elif right > 3 and wrong > 3:
            break