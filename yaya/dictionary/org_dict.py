from yaya import config
from yaya.collection.dict import DoubleArrayTrie
from yaya.collection.hmm import HMMMatrix
from yaya.common.nt import NTPattern, NT
from yaya.utility.singleton import singleton

__author__ = 'tony'


@singleton
class OrgDict:
    def __init__(self):
        self.trie = DoubleArrayTrie.load(config.ORG_DICT_NAME, enum_cls=NT)
        self.matrix = HMMMatrix.load(config.ORG_TR_PATH, NT)




@singleton
class NTPatternDict:
    def __init__(self):
        self.trie = DoubleArrayTrie()
        NTPattern.sort()
        self.trie.build(key=NTPattern)
