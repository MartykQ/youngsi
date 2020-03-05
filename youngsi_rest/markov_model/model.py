import itertools
import pickle
import random
from collections import defaultdict

from youngsi_rest.helpers import pick_by_weight, get_unique_words, reverse_lines, calculate_dict_probability
from youngsi_rest.markov_model.errors import TokenNotFound, RhymeNotFound

BEGIN = '__BEGIN__'
END = '__END__'


class MarkovModel:

    def __init__(self, corpus, n: int):
        self.n_base = n
        self._corpus = corpus
        self._model = defaultdict(dict)

    def _prepare_sentence(self, sentence: str) -> list:
        return [*[BEGIN] * self.n_base, *sentence.split(), *[END] * self.n_base]

    def fit_model(self) -> None:
        for line in self._corpus:
            sentence = self._prepare_sentence(line)
            for i, word in enumerate(sentence):
                *key, value = sentence[i:i+self.n_base+1]
                key = tuple(key)
                self._model[key][value] = self._model[key].get(value, 0) + 1

        for d_key in self._model:
            self._model[d_key] = calculate_dict_probability(self._model[d_key])
        self._model = dict(self._model)

    def get_next_token(self, token: tuple) -> str:
        try:
            choices = self._model[token]
        except KeyError:
            raise TokenNotFound("Token was not present in the corpus")
        return pick_by_weight(choices)

    def get_random_token(self):
        random_key = random.choice(list(self._model.keys()))
        return pick_by_weight(self._model[random_key])

    def get_random_start_token(self):
        return pick_by_weight(self._model[(BEGIN, )*self.n_base])

    def fit_rhymes(self) -> defaultdict:
        found_rhymes = defaultdict(set)
        unique_words = get_unique_words(self._corpus)
        for i, word in enumerate(unique_words):

            for last_n in range(2, 6):
                key = word[-last_n:]
                found_rhymes[key].add(word)

        # Converting to dictionary of {string: list} to support saving to json file
        found_rhymes = dict(found_rhymes)
        for key in found_rhymes:
            found_rhymes[key] = list(found_rhymes[key])
        return found_rhymes


class SongWriter:

    def __init__(self, n_base, forward_model, backward_model, rhymes):
        self.n_base = n_base
        self._forward_model = forward_model
        self._backward_model = backward_model
        self._rhymes = rhymes

    def _get_rhyming_word(self, word) -> str:
        choices = []
        for last_n in reversed(range(2, 6)):
            key = word[-last_n:]
            if self._rhymes[key]:
                choices.extend({random.choice(self._rhymes[key]) for w in range(last_n)})

        if choices:
            return random.choice(choices)
        else:
            raise RhymeNotFound

    def write_sentence(self, mode, first_word=None, max_tries=3, max_words=8):

        possible_sentences = []
        for i in range(max_tries):
            new_sentence = self._generate_sentence(mode=mode, first_word=first_word, max_words=max_words)
            possible_sentences.append(new_sentence)

        distribution = {k: len(k) for k in possible_sentences}
        distribution = calculate_dict_probability(distribution)

        return pick_by_weight(distribution)

    def _generate_sentence(self, mode='forward', first_word=None, max_words=15):
        models = {
            'forward': self._forward_model,
            'backward': self._backward_model
        }
        model = models[mode]
        sentence = Sentence()

        for _ in range(self.n_base):
            sentence.append(BEGIN)

        if not first_word:
            # If first word not privided chose random word from the model
            first_word = model.get_random_start_token()
            sentence.append(first_word)
        else:
            sentence.append(first_word)

        for i in range(max_words):
            token = sentence.get_last_n(self.n_base)
            try:
                next_token = model.get_next_token(token)
            except TokenNotFound:
                next_token = model.get_random_start_token()
                # possible_tokens = [pos_token for pos_token in model._model.keys() if sentence.get_last_n(1) in pos_token]
                # if possible_tokens:
                #     next_token = model.get_next_token(random.choice(possible_tokens))
                # else:
                #     next_token = model.get_random_start_token()

            sentence.append(next_token)
            if END in next_token:
                break

        sentence = sentence.clear()
        if mode == 'backward':
            return sentence.revert()
        return sentence

    def _generate_rhyming_lines(self, num_lines, max_tries=50):
        """
        :param num_lines: How many lines to generate
        :param max_tries: How many times try to generate first sentence with last word that has no rhyme
        :return: list o Sentences
        """

        rhyme = None
        for _ in range(max_tries):
            try:
                first_line = self.write_sentence(mode='forward')
                rhyme = self._get_rhyming_word(first_line.get_last_n(1)[0])
                break
            except RhymeNotFound:
                pass

        if not rhyme:
            raise RhymeNotFound

        lines = [first_line, ]

        for i in range(num_lines):
            next_sentence = self.write_sentence(mode='backward', first_word=rhyme)
            try:
                rhyme = self._get_rhyming_word(next_sentence.get_last_n(1)[0])
            except RhymeNotFound:
                rhyme = None
            lines.append(next_sentence)

        return lines

    def sing_a_song(self, num_verse=3, num_chorus_lines=6):

        chorus = self._generate_rhyming_lines(num_chorus_lines)
        song = [chorus, ]
        for i in range(num_verse):
            verse_a = self._generate_rhyming_lines(4)
            verse_b = self._generate_rhyming_lines(4)
            verse = list(itertools.chain.from_iterable((zip(verse_a, verse_b))))
            song.append(verse)
            song.append(chorus)

        for segment in song:
            print("_________")
            for line in segment:
                print(line)

        return song

    @classmethod
    def create_raper(cls, text_corpus_path, n_base):

        corpus = open(text_corpus_path, 'r', encoding='utf-8')
        forward_model = MarkovModel(corpus, n_base)
        forward_model.fit_model()

        corpus.seek(0)
        rhymes = forward_model.fit_rhymes()

        corpus = open(text_corpus_path, 'r', encoding='utf-8')
        backward_model = MarkovModel(reverse_lines(corpus), n_base)
        backward_model.fit_model()

        return cls(n_base, forward_model, backward_model, rhymes)

    @classmethod
    def load_raper(cls, path):
        f = open(path, 'rb')
        loaded_model = pickle.load(f)

        forward = MarkovModel([], loaded_model['n_base'])
        backward = MarkovModel([], loaded_model['n_base'])

        forward._model = loaded_model['forward']
        backward._model = loaded_model['backward']

        return cls(loaded_model['n_base'],
                   forward,
                   backward,
                   loaded_model['rhymes'])

    def save_raper(self, path):

        self._forward_model._corpus, self._backward_model._corpus = None, None
        saved_models = {
            'n_base': self.n_base,
            'forward': dict(self._forward_model._model),
            'backward': dict(self._backward_model._model),
            'rhymes': self._rhymes
        }
        f = open(path, 'wb')
        pickle.dump(saved_models, f)


class Sentence:

    def __init__(self):
        self.words = []

    def append(self, word):
        self.words.append(word)

    def get_last_n(self, n):
        return tuple(self.words[-n::])

    def revert(self):
        self.words.reverse()
        return self

    def clear(self):
        self.words = [word for word in self.words if word != BEGIN and word != END]
        return self

    def __str__(self):
        return " ".join(self.words)

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return repr(self.words)


if __name__ == '__main__':
    n1 = SongWriter.create_raper(text_corpus_path=r'D:\DATA\Projects\youngsi\corpus.txt', n_base=1)
    n2 = SongWriter.create_raper(text_corpus_path=r'D:\DATA\Projects\youngsi\corpus.txt', n_base=2)

    n1.save_raper(r'D:\DATA\Projects\youngsi\data\youngsi_n1.pkl')
    n2.save_raper(r'D:\DATA\Projects\youngsi\data\youngsi_n2.pkl')

