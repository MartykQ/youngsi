import random

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



def calculateDictProbability(dict):
    """Given a dictionary where values are quantity, returns a dictionary where values are probability of the key"""
    newDict = {}
    newDict.update(dict)
    total = 0

    for k, v in newDict.items():
        total += v


    for k,v in newDict.items():
        newDict[k] = v/total


    return newDict
