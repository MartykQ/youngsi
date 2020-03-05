import unittest
from youngsi_rest.markov_model.model import MarkovModel, SongWriter
from youngsi_rest.markov_model.errors import TokenNotFound


class TestSongWriter(unittest.TestCase):

    def test_int(self):
        self.song_writer = SongWriter.create_raper('D:\DATA\Projects\youngsi\corpus.txt', 1)

        print(self.song_writer._rhymes)
        print(self.song_writer._forward_model._model)
        print(self.song_writer._backward_model._model)
        print(self.song_writer._get_rhyming_word('wszedlem'))

    def test_generate_sentence(self):
        print(self.song_writer._generate_rhyming_lines(num_lines=7))


if __name__ == '__main__':
    unittest.main()