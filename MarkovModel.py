import random
from splitters import split_into_sentences
import re
import funcs as fn
import json
import random


BEGIN = "___BEGIN__"
END = "___END__"

class MarkovModel:

    def __init__(self, order, tekst):
        """
        :param order: number of base words
        :param tekst: txt file
        """
        self.order = order
        self.groupSize = self.order + 1
        self.text = tekst.readlines()
        self.allWords = []
        self.graph = {} #forward model
        self.graphReversed = {} #reversed model
        self.rhymesDict = {}    #rhymes previously found
        self.graphSafe = {}     # created when self.order > 1

        self.initializeModel()

        return


    def sentenceSplit(self, text):
        """markovify"""
        return split_into_sentences(text)

    word_split_pattern = re.compile(r"\s+")

    def word_split(self, sentence):
        return re.split(self.word_split_pattern, sentence)


    def generatePrimeList(self, text):
        if isinstance(text, str):
            sentences = self.sentenceSplit(text)
        else:
            sentences = []
            for line in text:
                sentences += self.sentenceSplit(line)

        primeList = list(map(self.word_split, sentences))

        return primeList



    def initializeModel(self):
        """
        training all needed models
        """


        self.trainModel()
        self.trainModelReversed()

        """
        getting all unique words
        
        for line in self.text:
            for element in line.split(' '):
                if element not in self.allWords:
                    self.allWords.append(element.replace("\n", ""))

        """

        if self.order >1:
            self.trainModelSafe()

        elif self.order == 1:
            self.graphSafe = self.graph

        plik = open("graphs/rymyWlasne4.json", "r", encoding="utf-8")
        self.rhymesDict = json.load(plik)




    def trainModel(self):

        corpus = self.generatePrimeList(self.text)

        for run in corpus:
            items = ([ BEGIN ] * self.order) + run + [ END ]
            for i in range(len(run) + 1):
                state = tuple(items[i:i+self.order])
                follow = items[i+self.order]

                if state not in self.graph:
                    self.graph[state] = {}

                if follow not in self.graph[state]:
                    self.graph[state][follow] = 0

                self.graph[state][follow] += 1

        for k in self.graph:
            self.graph[k] = fn.calculateDictProbability(self.graph[k])


    def trainModelReversed(self):

        corpus = self.generatePrimeList(self.text)

        for i in range(0,len(corpus)):
            corpus[i].reverse()

        for run in corpus:
            items = ([ BEGIN ] * self.order) + run + [ END ]
            for i in range(len(run) + 1):
                state = tuple(items[i:i+self.order])
                follow = items[i+self.order]
                if state not in self.graphReversed:
                    self.graphReversed[state] = {}

                if follow not in self.graphReversed[state]:
                    self.graphReversed[state][follow] = 0

                self.graphReversed[state][follow] += 1

        for k in self.graphReversed:
            self.graphReversed[k] = fn.calculateDictProbability(self.graphReversed[k])




    def makeSentence(self, startState = None, maxWords = 9, minWords = 4, max_tries = 6):
        """

        not optimalized at all

        :param startState: beggining of the sentence

        """
        result = []
        word_count = 0

        for i in range (self.order-1):
            result.append(BEGIN)

        if startState == None:
            result.append(self.getNextWord(startState))
            word_count = 1
        else:
            result.append(startState)
            word_count = 1

        tries = 0

        while tries < max_tries:

            while result[-1] != END and word_count < maxWords:

                nextWord = self.getNextWord(result[-self.order:])

                result.append(nextWord)
                word_count += 1
                if word_count==maxWords:
                    result.append(END)
                    word_count += 1

            result = list(filter((BEGIN).__ne__, result))
            result = list(filter((END).__ne__, result))
            sentence = " ".join(result)
            tries += 1

            if len(sentence)>4:
                return sentence

        return sentence

    def makeSentenceReversed(self, startState = None, maxWords = 9, minWords = 4, max_tries=6):
        result = []
        word_count = 0
        for i in range (self.order-1):
            result.append(BEGIN)

        if startState == None:
            result.append(self.getPrevWord(startState))
            word_count = 1
        else:
            result.append(startState)

        tries = 0

        while tries<max_tries:

            while result[-1] != END and word_count < maxWords:
                nextWord = self.getPrevWord(result[-self.order:])
                result.append(nextWord)
                word_count += 1
                if word_count==maxWords:
                    result.append(END)
                    word_count += 1

            result = list(filter((BEGIN).__ne__, result))
            result = list(filter((END).__ne__, result))

            result.reverse()
            sentence = " ".join(result)

            tries +=1

            if len(sentence) > 3:
                return sentence

        return sentence


    def findRhymingWord(self, word):

        if word in self.rhymesDict:

            if(len(self.rhymesDict[word])>0):

                rhyme = random.choice(self.rhymesDict[word])
                return rhyme
            else:
                return None
        else:
            return None



    def getNextWord(self, previousWord = None):

        if previousWord == None:
            key = tuple([BEGIN]*self.order)
        else:
            key = tuple(previousWord)

        nextWord = fn.weighted_random_by_dct(self.graph[key])

        return nextWord



    def getPrevWord(self, nextWord = None):
        """
        uses reversed model. Looks for next (previous word). When self.order > 1 and fails to find
        word in prime model, uses graphSafe model which is model trained with 1 order. When it fails too,
        it continues as it started the sentence from scratch

        :param nextWord:
        :return:
        """

        if nextWord == None:
            key = tuple([BEGIN]*self.order)
        else:
            key = tuple(nextWord)

        try:
            prevWord = fn.weighted_random_by_dct(self.graphReversed[key])
        except KeyError: #didnt find this key in prime model

            try:
                key = (key[-1],)
                prevWord = fn.weighted_random_by_dct(self.graphSafe[key])
            except KeyError: #didnt find in 1-order model
                key = tuple([BEGIN],) #starts from scratch
                prevWord = fn.weighted_random_by_dct(self.graphSafe[key])

        return prevWord


    def singVerse(self):
        """
        TO DO: customization

        writes simple Verse. Geneartes 3 x 3 sentences ending with rhyming word (if possible)

        """
        verse = []
        for i in range(1,4):
            line = self.makeSentence().split()
            verse.append(line)
            line2 = self.makeSentenceReversed(self.findRhymingWord(verse[-1][-1])).split()
            verse.append(line2)
            line3= self.makeSentenceReversed(self.findRhymingWord(verse[-1][-1])).split()
            verse.append(line3)

        return verse


    def singChor(self, line_numb):

        chor = []

        while True:
            """
            Generates first line. Last word of the line should be loneger than 3 chars. (Better rhymes)
            """
            line = self.makeSentenceReversed().split()
            chor.append(line)

            if len(chor[-1][-1]) > 3:
                break
            else:
                del chor[-1]

        for i in range(0,line_numb):

            line2 = self.makeSentenceReversed(self.findRhymingWord(chor[-1][-1])).split()
            chor.append(line2)

        return chor


    def dropThatBeat(self, verse_numb, line_numb):

        """sings a song"""

        song = []
        refren = self.singChor(line_numb)
        refren.insert(0, ['<br>REFREN <br>'])

        for i in range(0, verse_numb):
            zwrotka = self.singVerse()
            zwrotka.insert(0, ['<br>ZWROTKA <br>'])
            song.append(zwrotka)
            song.append(refren)

        final = ""

        for line in song:
            for line2 in line:
                final += " ".join(line2) + "<br>"

        final.replace('\n', '<br>')
        return final




    def trainModelSafe(self):

        corpus = self.generatePrimeList(self.text)

        for i in range(0,len(corpus)):
            corpus[i].reverse()

        for run in corpus:
            items = ([ BEGIN ] * 1) + run + [ END ]
            for i in range(len(run) + 1):
                state = tuple(items[i:i+1])
                follow = items[i+1]
                if state not in self.graphSafe:
                    self.graphSafe[state] = {}

                if follow not in self.graphSafe[state]:
                    self.graphSafe[state][follow] = 0

                self.graphSafe[state][follow] += 1

        for k in self.graphSafe:
            self.graphSafe[k] = fn.calculateDictProbability(self.graphSafe[k])





