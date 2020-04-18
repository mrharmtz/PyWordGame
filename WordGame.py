import random
import re
import time


class WordGame:

    WORD_FILTER = re.compile(r'[^a-zA-Z \-\(\)]')
    WORD_SPLITTER = re.compile(r'\-|\(|\)| ')

    def __init__(self):

        word_collection = {}

        with open('english_dictionary.txt', 'r') as fd:
            for line in fd:
                value = self.WORD_FILTER.sub('', line).lower().strip()
                if value == '':
                    continue
                words = self.WORD_SPLITTER.split(value)
                for word in words:
                    if len(word) in word_collection:
                        word_collection[len(word)].add(word)
                    else:
                        word_collection[len(word)] = set([word])

        self.__word_db = {}

        for key, value in word_collection.items():
            self.__word_db[key] = list(value)

        self.__score = None
        self.__generated_amount = None
        self.__start_time = None
        self.__average_time = None
        self.reset()

    def reset(self):
        self.__score = 0
        self.__generated_amount = 0
        self.__start_time = 0.0
        self.__average_time = 0.0

    def generate(self, difficulty=[3], word_count=1):
        self.__start_time = time.time()
        return ' '.join(random.choices(self.__word_db[random.choice(difficulty)], k=word_count))

    def point(self, word):
        sum_time = self.__average_time * self.__generated_amount
        self.__generated_amount += 1
        self.__average_time = (sum_time + (time.time() - self.__start_time))/self.__generated_amount
        self.__score += len(word)

    @property
    def start_time(self):
        return self.__start_time

    @property
    def score(self):
        return self.__score

    @property
    def average_time(self):
        return self.__average_time

