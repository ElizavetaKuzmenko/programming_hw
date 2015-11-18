KEYBOARD = {'q': 'wsa', 'w': 'qase', 'e': 'wsdfr', 'r': 'edfgt', 't': 'rfghy', 'y': 'tghju', 'u': 'yhjki', 'i': 'ujklo',
            'o': 'iklp', 'p': 'ol', 'a': 'qwsz', 's': 'qazxcdew', 'd': 'ewsxcvfr', 'f': 'redcvbgt', 'g': 'trfvbnhy',
            'h': 'ytgbnmju', 'j': 'uyhnnmki', 'k': 'iujmmlo', 'l': 'oikp', 'z': 'asdx', 'x': 'zasdc', 'c': 'xsdfv',
            'v': 'gfcb', 'b': 'hgfvn', 'n': 'jhgbm', 'm': 'lkjhn'}

def weight(symb1, symb2):
    if symb2 in KEYBOARD[symb1]:
        return 1
    else:
        return 2

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
            ins = table[i][j + 1] + w
            delete = table[i + 1][j] + w
            table[i + 1][j + 1] = min(edit,
                                      ins, delete)
    return table[len(word2)][len(word1)]


def most_close(word, vocab):
    dists = {}
    for v in vocab:
        ld = levenshtein(word, v)
        try:
            dists[ld].append(v)
        except:
            dists[ld] = [v]
    min_ld = min(dists.keys())
    res = dists[min_ld]
    return res

if __name__ == '__main__':
    word1 = 'daisy'
    word2 = 'dayzy'
    print(word1, word2, levenshtein(word1, word2))
    word3 = 'dayly'
    print(word1, word3, levenshtein(word1, word3))