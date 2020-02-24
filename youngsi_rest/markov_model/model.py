from collections import defaultdict
from youngsi_rest.helpers import pick_by_weight, get_unique_words
from youngsi_rest.markov_model.errors import TokenNotFound

BEGIN = '__BEGIN__'
END = '__END__'


class MarkovModel:

    def __init__(self, corpus, n: int):
        self.n_base = n
        self._corpus = corpus
        self._model = defaultdict(dict)
        self._rhymes = defaultdict(set)

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

    def _fit_rhymes(self):
        self._corpus.seek(0)
        unique_words = get_unique_words(self._corpus)


class SongWriter:

    def __init__(self, forward_model, backward_model):
        self._forward_model = forward_model
        self._backward_model = backward_model

    def write_sentence_forward(self, first_word=None):
        pass

    def write_sentence_backward(self, first_word=None):
        pass

    def _generate_sentence(self, mode='forward', first_word=None):
        models = {
            'forward': self._forward_model,
            'backward': self._backward_model
        }
        model = models[mode]

        sentence = Sentence()

        if not first_word:



class Sentence:

    def __init__(self, first_word=None):
        self.words = [first_word]

    def append(self, word):
        self.words.append(word)



