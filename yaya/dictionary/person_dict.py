from yaya import config
from yaya.collection.dict import DoubleArrayTrie
from yaya.collection.hmm import HMMMatrix
from yaya.common.nr import NRPattern, NR
from yaya.utility.singleton import singleton

__author__ = 'tony'


@singleton
class PersonDict:
    def __init__(self):
        self.trie = DoubleArrayTrie.load(config.PERSON_DICT_NAME, enum_cls=NR)
        self.matrix = HMMMatrix.load(config.PERSON_TR_PATH, NR)


@singleton
class NRPatternDict:
    def __init__(self):
        self.trie = DoubleArrayTrie()
        NRPattern.sort()
        self.trie.build(key=NRPattern)