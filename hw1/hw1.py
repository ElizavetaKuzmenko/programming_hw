# coding: utf-8
# python3.4
__author__ = 'liza'

import time

# 1. Использовать везде, где возможно, множества и словари!
# 2. Часто используемые регулярные выражения -- reg = re.compile('...', flags=...), m = reg.search(text)
# 3. Искать в документах с помощью обратного индекса
# 4. Использовать эффективные алгоритмы!
# 5. Ленивые вычисления!


# Задание:
# 1. Программа получает список слов от пользователей, а затем для каждого печатает все сниппеты этого слова (+- 1 строчка)
# 2. -//- получает то же самое, а затем ищет в файлах слова, которые зарифмованы с данным (в одном стихотворении +- 2 строки)


def poem_index(text):
    p_index = {}
    i = 0
    for line in text:
        words = line.strip().split()
        for word in words:
            word = word.strip(characters)
            try:
                p_index[word].append(i)
            except:
                p_index[word] = [i]
        i += 1
    return p_index

characters = '.,;:?!-()[]{}"\' '
queries = open('queries.txt', 'r', encoding='utf-8')
texts = open('long_poem.txt', 'r', encoding='utf-8')
snippets = open('snippets.txt', 'w', encoding='utf-8')
rhymes_f = open('rhymes.txt', 'w', encoding='utf-8')
ind = poem_index(texts)
texts.close()
texts = open('long_poem.txt', 'r', encoding='utf-8')
text_lines = texts.readlines()


def getSnippet(num):
    if num != 0 or num != len(text_lines):
        snippet = text_lines[int(num) - 1] + text_lines[int(num)] + text_lines[int(num) + 1]
    elif num == 0:
        snippet = text_lines[int(num)] + text_lines[int(num) + 1]
    elif num == len(text_lines):
        snippet = snippet = text_lines[int(num) - 1] + text_lines[int(num)]
    return snippet


def getRhymes(query, lines):
    rhymes = set()
    for num in lines:
        poem_line = text_lines[int(num)]
        #all_lines = text_lines[int(num) - 2] + text_lines[int(num) - 1] + text_lines[int(num)] + text_lines[int(num) + 1] + text_lines[int(num) + 2]
        if query == poem_line.strip().split()[-1].lower().strip('.,;:?!-()[]{}"\' '):
            possible_rhymes = [text_lines[int(num) - 2].strip().split()[-1], text_lines[int(num) - 1].strip().split()[-1],
                               text_lines[int(num) + 1].strip().split()[-1], text_lines[int(num) + 2].strip().split()[-1]]
            possible_rhymes = [x.strip('.,;:?!-()[]{}"\' ') for x in possible_rhymes]
            possible_rhymes = [x for x in possible_rhymes if len(x) > 0]
            for word in possible_rhymes:
                if isRhyme(query, word):
                    rhymes.add(word)
    return rhymes


def isRhyme(query, word):
    dic = {'б': 'п', 'в': 'ф', 'г': 'к', 'д': 'т', 'з': 'с', 'ж': 'ш', 'о': 'а', 'е': 'и', 'п': 'б', 'ф': 'в', 'к': 'г',
           'т': 'д', 'с': 'з', 'ш': 'ж', 'а': 'о', 'и': 'е'}
    if query[-2:] == word[-2:] or ((query[-1] in dic and word[-1] in dic) and dic[query[-1]] == dic[word[-1]]
                                   and query[-2] == word[-2]):
        return True
    else:
        return False


def main():
    for line in queries:
        query = line.strip()
        lines = ind[query]
        rhymes_f.write(query + '\t')
        rhyme_lines = ''
        snippets.write(query + '\n')
        snippets_lines = ''
        if len(lines) > 0:
            t1 = time.time()
            rhymes = getRhymes(query, lines)
            t2 = time.time()
            for rhyme in rhymes:
                rhyme_lines += rhyme + ', '
            t3 = time.time()
            for num in lines:
                snippets_lines += getSnippet(num) + '\n'
            t4 = time.time()
            print('snippets time', t4 - t3)
            print('rhyme time ', t2 - t1)
        rhymes_f.write(rhyme_lines[:-2] + '\n')
        snippets.write(snippets_lines + '\n')
    snippets.close()
    rhymes_f.close()

if __name__ == '__main__':
    main()
