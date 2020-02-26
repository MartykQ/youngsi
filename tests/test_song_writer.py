import unittest
from youngsi_rest.markov_model.model import MarkovModel, SongWriter
from youngsi_rest.markov_model.errors import TokenNotFound


class TestSongWriter(unittest.TestCase):

    def setUp(self) -> None:
        self.song_writer = SongWriter.create_raper('test_corpus.txt', 1)

    def tearDown(self) -> None:
        pass

    def test_int(self):
        print(self.song_writer._rhymes)
        print(self.song_writer._forward_model._model)
        print(self.song_writer._backward_model._model)
        print(self.song_writer._get_rhyming_word('wszedlem'))


if __name__ == '__main__':
    unittest.main()