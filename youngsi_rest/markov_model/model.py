from collections import defaultdict
from youngsi_rest.helpers import pick_by_weight, get_unique_words, does_rhyme, reverse_lines
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

    def fit_rhymes(self) -> defaultdict:
        found_rhymes = defaultdict(set)
        unique_words = get_unique_words(self._corpus)
        for word in unique_words:
            for potential_rhyme in unique_words:
                if does_rhyme(word, potential_rhyme):
                    found_rhymes[word].add(potential_rhyme)

        return found_rhymes


class SongWriter:

    def __init__(self, forward_model, backward_model, rhymes):
        self._forward_model = forward_model
        self._backward_model = backward_model
        self._rhymes = rhymes

    def _get_rhyming_word(self, word):
        choices = self._rhymes[word]
        if not choices:
            raise RhymeNotFound

        rhymes_distribution = {}

        for

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
            pass

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

        return cls(forward_model, backward_model, rhymes)


class Sentence:

    def __init__(self, first_word=None):
        self.words = [first_word]

    def append(self, word):
        self.words.append(word)



