import numpy as np
from itertools import chain

MIN_RHYME = 2


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


if __name__ == '__main__':
    print(does_rhyme('kot', 'płot'))