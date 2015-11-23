# coding: utf-8
__author__ = 'liza'

import re
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import mlab
from pymystem3 import Mystem
m = Mystem()

from genre_by_pos import nouns, adjectives, verbs, pronouns, adverbs
from genre_by_letters import words, vowel
