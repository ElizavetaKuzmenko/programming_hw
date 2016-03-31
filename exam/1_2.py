# coding: utf-8

import re

a = ('S', ('NP', ('A', 'little'), ('NP', 'boys')), ('VP', ('VP', 'run'), ('JJ', 'fast')))
b = ('S', ('NP', ('A', 'little'), ('NP', ('NPC', ('NP', 'boy'), ('CC', 'and')), ('NP', 'girl'))), ('VP', 'run'))
c = ('S', ('NP', ('A', 'little'), ('NP', ('NPC', ('NP', 'girls'), ('CC', ',')), ('NP', ('NPC', ('NP', 'boys'), ('CC', 'and')), ('NP', 'dogs')))), ('VP', 'run'))
d = ('S', ('NP', ('NPC', ('NP', 'girls'), ('CC', 'and')), ('NP', 'boys')), ('VP', ('VP', 'run'), ('NP', ('A', 'nice'), ('NP', 'farm'))))
e = ('S', ('NP', 'dogs'), ('VP', ('VP', 'jump'), ('JJ', 'not')))
f = ('VP', ('VP', ('VP', 'fear'), ('JJ', 'not')), ('NP', ('A', 'my'), ('NP', ('A', 'fair'), ('NP', 'lady'))))

nps = []


def tree_depth(tree):
    #print(tree)
    try:
        if not type(tree) is str:
            left_depth = tree_depth(tree[1])
        else:
            left_depth = 0
    except:
        left_depth = 0
    try:
        if not type(tree) is str:
            right_depth = tree_depth(tree[2])
        else:
            right_depth = 0
    except:
        right_depth = 0
    return max(left_depth, right_depth) + 1


def all_nps(tree):
    #print(tree, tree[0])
    if tree[0] == 'NP':
        #print(tree)
        nps.append(tree)
        #print(nps)
    try:
        if not type(tree) is str:
            left_els = all_nps(tree[1])
    except:
        pass
    try:
        if not type(tree) is str:
            right_els = all_nps(tree[2])
    except:
        pass
    nps_words = []
    for np in nps:
        nps_words.append(find_words(np))
    return nps_words


def find_words(np):
    words = ''
    if len(np) == 2:
        return words + np[1] + ' '
    words += find_words(np[1]) + ' '
    words += find_words(np[2]) + ' '
    return re.sub(' +', ' ', words.strip(' '))


if __name__ == '__main__':
    print(all_nps(b))