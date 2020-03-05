import unittest
from youngsi_rest.helpers import pick_by_weight, get_unique_words, does_rhyme


class TestHelpers(unittest.TestCase):

    def test_pick_by_weight(self):
        d = {'a': 1, 'b': 2}
        results = []
        for i in range(100):
            result = pick_by_weight(d)
            results.append(result)

        self.assertGreater(results.count('b'), results.count('a'))

    def test_unique_words(self):
        corpus = open('test_corpus.txt', 'r', encoding='utf-8')
        print(get_unique_words(corpus))

    def test_does_rhyme(self):
        self.assertEqual(does_rhyme('kot', 'płot'), True)
        self.assertEqual(does_rhyme('kot', 'samolot'), True)
        self.assertEqual(does_rhyme('kot', 'alasdmot'), True)

        self.assertEqual(does_rhyme('kot', 'kot'), False)

        self.assertEqual(does_rhyme('kot', 'asdasd'), False)
        self.assertEqual(does_rhyme('kot', 's'), False)
        self.assertEqual(does_rhyme('kot', 'kotn'), False)
        self.assertEqual(does_rhyme('kot', 'kotek'), False)

        self.assertEqual(does_rhyme('ot', ''), False)
        self.assertEqual(does_rhyme('asdasd', ''), False)
        self.assertEqual(does_rhyme('kot', 'kotek'), False)


if __name__ == '__main__':
    unittest.main()