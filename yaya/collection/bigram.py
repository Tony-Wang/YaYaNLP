# coding=utf-8
from __future__ import absolute_import

import time

from yaya import config
from yaya.collection.dict import CoreDict
from yaya.const import logger
from yaya.utility.singleton import singleton

__author__ = 'tony'


class BiGramTable:
    def __init__(self):
        self.start = []
        self.pair = []

    def get_bifreq(self, pre_word, next_word):
        pre_word_id = pre_word if type(pre_word) is int else CoreDict().trie.exact_match_search(pre_word)
        if pre_word_id == -1:
            return 0
        next_word_id = next_word if type(next_word) is int else CoreDict().trie.exact_match_search(next_word)
        if next_word_id == -1:
            return 0
        index = binary_search(self.pair, self.start[pre_word_id],
                              self.start[pre_word_id + 1] - self.start[pre_word_id],
                              next_word_id)
        if index < 0:
            return 0
        index <<= 1
        return self.pair[index + 1]

    @staticmethod
    def load(filename=config.CORE_BIGRAM_NAME):
        start = time.time()
        logger.info(u"开始加载核心二元语法词表")
        import os
        if os.path.exists(filename + config.DICT_BIN_EXT):
            return BiGramTable.load_bin(filename + config.DICT_BIN_EXT)
        else:
            table = BiGramTable.build(filename)
            import cPickle as Pickle
            with open(filename + config.DICT_BIN_EXT, 'w') as f:
                Pickle.dump(table, f)
            return table
        logger.info(u"加载核心二元语法词表完毕，耗时%s", time.time() - start)

    @staticmethod
    def load_bin(filename):
        import cPickle as Pickle
        with open(filename, 'r') as f:
            bigram = Pickle.load(f)
            f.close()
            return bigram

    @staticmethod
    def build(filename):
        import codecs
        f = codecs.open(filename, 'r', 'utf-8')
        pre_word_map = {}
        max_word_id = CoreDict().trie.word_size()
        total = 0
        while True:
            line = f.readline()
            if not line:
                break
            params = line.split()
            if params.__len__() != 2:
                continue
            two_word = params[0].split('@', 2)
            if two_word.__len__() != 2:
                continue

            pre_word_id = CoreDict().trie.exact_match_search(two_word[0])
            if pre_word_id == -1:
                continue
            next_word_id = CoreDict().trie.exact_match_search(two_word[1])
            if next_word_id == -1:
                continue
            if pre_word_id not in pre_word_map:
                pre_word_map[pre_word_id] = {}
            next_word_map = pre_word_map.get(pre_word_id)
            next_word_map[next_word_id] = int(params[1])
            total += 2
        f.close()

        table = BiGramTable()
        table.start = [0] * (max_word_id + 1)
        table.pair = [0] * total
        offset = 0
        for i in range(max_word_id):
            next_word_map = pre_word_map.get(i, None)
            if next_word_map is not None:
                key_list = next_word_map.keys()
                key_list.sort()
                for k in key_list:
                    index = offset << 1
                    table.pair[index] = k
                    table.pair[index + 1] = next_word_map[k]
                    offset += 1
            table.start[i + 1] = offset
        return table


def binary_search(a, from_index, length, key):
    low = from_index
    high = from_index + length - 1
    while low <= high:
        mid = (low + high) >> 1
        mid_val = a[mid << 1]
        if mid_val < key:
            low = mid + 1
        elif mid_val > key:
            high = mid - 1
        else:
            return mid
    return -(low + 1)


@singleton
class CoreBiGramTable:
    def __init__(self):
        self.table = BiGramTable.load()
