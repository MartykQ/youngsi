from collections import defaultdict
import random

from youngsi_rest.helpers import pick_by_weight, get_unique_words, does_rhyme, reverse_lines, rate_rhyme
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

    def get_next_token(self, token: tuple) -> str:
        choices = self._model[token]
        if not choices:
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
        for word in unique_words:
            for potential_rhyme in unique_words:
                if does_rhyme(word, potential_rhyme):
                    found_rhymes[word].add(potential_rhyme)

        return found_rhymes


class SongWriter:

    def __init__(self, n_base, forward_model, backward_model, rhymes):
        self.n_base = n_base
        self._forward_model = forward_model
        self._backward_model = backward_model
        self._rhymes = rhymes

    def _get_rhyming_word(self, word):
        choices = self._rhymes[word]
        if not choices:
            raise RhymeNotFound

        rhymes_distribution = {}

        for rhyme in choices:
            rhymes_distribution[rhyme] = rate_rhyme(word, rhyme)

        return pick_by_weight(rhymes_distribution)

    def write_sentence_forward(self, first_word=None):
        pass

    def write_sentence_backward(self, first_word=None):
        pass

    def _generate_sentence(self, mode='forward', first_word=None, max_tries=30):
        models = {
            'forward': self._forward_model,
            'backward': self._backward_model
        }
        model = models[mode]
        sentence = Sentence()

        # TODO appending BEGIN

        if not first_word:
            # If first word not privided chose random word from the model
            first_word = model.get_random_start_token()
            sentence.append(first_word)
        else:
            sentence.append(first_word)

        for i in range(max_tries):
            token = sentence.get_last_n(self.n_base)
            try:
                next_token = model.get_next_token(token)
            except TokenNotFound as e:
                possible_tokens = [pos_token for pos_token in model.keys() if pos_token[-1] == sentence.get_last_n(1)]
                if possible_tokens:
                    next_token = model.get_next_token(random.choice(possible_tokens))
                else:
                    next_token = model.get_random_start_token()

            sentence.append(next_token)
            if END in next_token:
                return sentence

        sentence.append(END)
        return sentence

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


class Sentence:

    def __init__(self, first_word=None):
        self.words = [first_word]

    def append(self, word):
        self.words.append(word)

    def get_last_n(self, n):
        return tuple(self.words[-n::])



