import unittest
from youngsi_rest.markov_model.model import MarkovModel, SongWriter
from youngsi_rest.markov_model.errors import TokenNotFound
import random
song_writer_youngsi_v1 = None
song_writer_youngsi_v2 = None
import time

class TestSongWriter(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global song_writer_youngsi_v1, song_writer_youngsi_v2
        start = time.clock()

        # song_writer_youngsi_v1 = SongWriter.load_raper(r'D:\DATA\Projects\youngsi\youngsi_rest\markov_model\youngsi_n1')
        song_writer_youngsi_v2 = SongWriter.load_raper(r'D:\DATA\Projects\youngsi\youngsi_rest\markov_model\youngsi_n2')

        ellapsed = time.clock()
        print(f"Took {start-ellapsed} to load the model ")

    def tearDown(self) -> None:
        pass

    def setUp(self) -> None:
        # self.test_model_1 = SongWriter.create_raper('test_corpus.txt', 1)
        self.test_model_2 = SongWriter.create_raper('test_corpus.txt', 2)

    # def test_int(self):
    #     print(song_writer_youngsi_v1._get_rhyming_word('franek'))
    #     print(song_writer_youngsi_v2._get_rhyming_word('franek'))
    #
    # def test_get_rhyming_word(self):
    #     dat = list(song_writer_youngsi_v1._rhymes.keys())[:150]
    #     random.shuffle(dat)
    #     print(dat)
    #
    #     start = time.clock()
    #     for word in dat:
    #         x = song_writer_youngsi_v1._get_rhyming_word(word)
    #     end = time.clock()
    #
    #     print(f"Took {end-start} to find rhymes for 150words")
    #
    # def test_generate_sentence(self):
    #     print(song_writer_youngsi_v1._generate_rhyming_lines(num_lines=7))

    def test_write_song(self):
        start = time.clock()

        # print(song_writer_youngsi_v1.sing_a_song())
        print("N2****************")
        print(song_writer_youngsi_v2.sing_a_song())


        ellapsed = time.clock()
        print(f"Took {ellapsed-start}")


