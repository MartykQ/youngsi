import numpy as np
from itertools import chain
import random
MIN_RHYME = 2


def pick_by_weight_legacy(d):
    d_choices = []
    d_probs = []
    for k, v in d.items():
        d_choices.append(k)
        d_probs.append(v)
    d_probs = [float(v/sum(d_probs)) for v in d_probs]
    return np.random.choice(d_choices, 1, p=d_probs)[0]


def pick_by_weight(d):
    """Given a key, value dict, where value is probability/quantity returns one key
    with given probabilty
    """
    rand_val = random.random()
    total = 0
    for k, v in d.items():
        total += v
        if rand_val <= total:
            return k
    # assert False, 'unreachable'


def get_unique_words(corpus):
    uniques = list(set(chain(*(line.split() for line in corpus if line))))
    return uniques


def does_rhyme(word: str, potential_rhyme: str) -> bool:
    if len(potential_rhyme) < MIN_RHYME or len(word) < MIN_RHYME:
        return False
    for i in reversed(range(len(word)+1)):
        if i < MIN_RHYME:
            return False
        if potential_rhyme.endswith(word[-i:]) and word != potential_rhyme:
            return True

    return False


def reverse_lines(text_file):
    for line in text_file:
        yield ' '.join(reversed(line.split()))


def count_syllabels():
    # TODO is it possible?
    raise NotImplementedError


def rate_rhyme(word, rhyme):
    return len(rhyme)


def weighted_random_by_dct(dct):
    """Given a key, value dict, where value is probability/quantity returns one key
    with given probabilty
    """
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'


def calculate_dict_probability(dict):
    """Given a dictionary where values are quantity, returns a dictionary where values are probability of the key"""
    newDict = {}
    newDict.update(dict)
    total = 0

    for k, v in newDict.items():
        total += v

    for k,v in newDict.items():
        newDict[k] = v/total

    return newDict


if __name__ == '__main__':

    print(rate_rhyme('kot', 'płot'))
    print(rate_rhyme('kot', 'kot'))
    print(rate_rhyme('kot', 'samolott'))

    print(rate_rhyme('samolot', 'kot'))
    print(rate_rhyme('kaszolot', 'samolot'))