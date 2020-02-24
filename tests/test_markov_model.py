import unittest
from youngsi_rest.markov_model.model import MarkovModel


class TestMarkov2(unittest.TestCase):

    def setUp(self) -> None:
        corpus = open('test_corpus.txt', 'r', encoding='utf-8')
        self.markov = MarkovModel(corpus, 2)

    def tearDown(self) -> None:
        pass

    def test_prepare_sentence(self):
        print(self.markov._prepare_sentence('koza z bobra'))
        self.assertEqual(0, 0)

    def test_fit_model(self):
        self.markov.fit_model()
        print(self.markov._forward_model)

if __name__ == '__main__':
    unittest.main()