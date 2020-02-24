import numpy as np
from itertools import chain


def pick_by_weight(d):
    d_choices = []
    d_probs = []
    for k, v in d.items():
        d_choices.append(k)
        d_probs.append(v)
    d_probs = [float(v/sum(d_probs)) for v in d_probs]
    return np.random.choice(d_choices, 1, p=d_probs)[0]


def get_unique_words(corpus):
    uniques = set(chain(*(line.split() for line in corpus if line)))
    return uniques