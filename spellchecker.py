# coding: utf-8
__author__ = 'liza'

neighbors_forward = {}
neighbors_back = {}
forward = ['йцукенгшщзхъ', 'фывапролджэ', 'ячсмитьбю']
back = ['ъхзщшгнекуцй', 'эждлорпавыф', 'юбьтимсчя']
for row in forward:
    neighbors_forward.update(dict(zip(row, row[1:])))
for row in back:
    neighbors_back.update(dict(zip(row, row[1:])))

def levenshtein(word1, word2):
    table = [[j for j in range(len(word1) + 1)]] +\
            [[i + 1] + [None] * len(word1)
             for i in range(len(word2))]

    for i in range(len(word2)):
        for j in range(len(word1)):
            w = weight(word1[j], word2[i])
            if word1[j] == word2[i]:
                edit = table[i][j]
            else:
                edit = table[i][j] + w
            ins = table[i][j + 1] + 1
            delete = table[i + 1][j] + 1
            table[i + 1][j + 1] = min(edit,
                                      ins, delete)
    return table[len(word2)][len(word1)]

def weight(symb1, symb2):
    try:
        if neighbors_forward[symb1] == symb2:
            return 0.5
    except KeyError:
        try:
            if neighbors_back[symb2] == symb1:
                return 0.5
        except KeyError:
            return 1
    return 1

def most_close(word, vocab):
    dists = {}
    for v in vocab:
        ld = levenshtein(word, v)
        try:
            dists[ld].append(v)
        except:
            dists[ld] = [v]
    result = {}
    for dist in sorted(dists):
        for word in dists[dist]:
            if len(result) < 3:
                result[word] = dist
            else:
                break
        if len(result) == 3:
            break
    return result

if __name__ == '__main__':
    vocab = set()
    with open('words.txt', encoding='utf-8') as words:
        for word in words:
            vocab.add(word.strip())
    read_word = input('Введите слово: ')
    result = most_close(read_word, vocab)
    for r in result:
        print(r, result[r])