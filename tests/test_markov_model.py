import unittest
from youngsi_rest.markov_model.model import MarkovModel
from youngsi_rest.markov_model.errors import TokenNotFound


class TestMarkovModel(unittest.TestCase):

    def setUp(self) -> None:
        self.corpus = open('test_corpus.txt', 'r', encoding='utf-8')
        self.markov_2 = MarkovModel(self.corpus, 2)
        self.markov_1 = MarkovModel(self.corpus, 1)


    def tearDown(self) -> None:
        pass

    def test_prepare_sentence(self):
        result_1 = self.markov_1._prepare_sentence('koza z bobra')
        result_2 = self.markov_2._prepare_sentence('koza z bobra')
        self.assertEqual(result_1, ['__BEGIN__', 'koza', 'z', 'bobra', '__END__'])
        self.assertEqual(result_2, ['__BEGIN__', '__BEGIN__', 'koza', 'z', 'bobra', '__END__', '__END__'])

    def test_fit_model(self):
        self.markov_1.fit_model()
        self.corpus.seek(0)
        self.markov_2.fit_model()

        print(self.markov_1._model)
        print(self.markov_2._model)
        print(self.markov_1.get_random_token())
        print(self.markov_2.get_random_token())
        print(self.markov_2.get_random_start_token())
        print(self.markov_1.get_random_start_token())

    def test_get_next_token(self):
        self.corpus.seek(0)
        model = MarkovModel(self.corpus, 1)
        model.fit_model()
        self.assertEqual(model.get_next_token(('test001', )), '__t001__')
        with self.assertRaises(TokenNotFound):
            model.get_next_token(('asdasdas12312asdd12asd', ))



if __name__ == '__main__':
    unittest.main()