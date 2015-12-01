from yaya.common.ns import NS, NSPattern
from yaya import config
from yaya.collection.dict import DoubleArrayTrie
from yaya.collection.hmm import HMMMatrix
from yaya.utility.singleton import singleton

__author__ = 'tony'


@singleton
class PlaceDict:
    def __init__(self):
        self.trie = DoubleArrayTrie.load(config.PLACE_DICT_NAME)
        self.matrix = HMMMatrix.load(config.PLACE_TR_PATH, NS)


@singleton
class NSPatternDict:
    def __init__(self):
        self.trie = DoubleArrayTrie()
        NSPattern.sort()
        self.trie.build(key=NSPattern)
