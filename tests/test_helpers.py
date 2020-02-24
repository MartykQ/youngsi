import unittest
from youngsi_rest.helpers import pick_by_weight, get_unique_words


class TestHelpers(unittest.TestCase):

    def test_pick_by_weight(self):
        d = {'a': 1, 'b': 2}
        result = pick_by_weight(d)

    def test_unique_words(self):
        corpus = open('test_corpus.txt', 'r', encoding='utf-8')
        print(get_unique_words(corpus))

if __name__ == '__main__':
    unittest.main()