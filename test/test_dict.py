# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from yaya.collection.dict import *
from yaya.common.nr import NRPattern
import yaya.config
from yaya.dictionary.person_dict import PersonDict, NRPatternDict

__author__ = 'tony'


class TestDoubleArrayTrie(TestCase):
    def test_fetch(self):
        trie = DoubleArrayTrie()
        words = []
        words.append(u"一举")
        words.append(u"一举一动")
        words.append(u"一举成名")
        words.append(u"一举成名天下知")
        words.append(u"啊")
        words.append(u"埃及")
        words.append(u"阿拉伯")
        words.append(u"阿拉伯人")
        words.append(u"阿根廷")
        words.append(u"阿胶")
        words.sort()
        trie.build(key=words, v=['一','一','一','一','二','三','四','四','四','四'])
        self.assertGreater(trie.exact_match_search(u"一举一动"),0)
        self.assertGreater(trie.exact_match_search(u"阿拉伯"),0)
        self.assertGreater(trie.exact_match_search(u"阿拉伯人"),0)

    def test_load_dict(self):
        trie = DoubleArrayTrie()
        trie.build(key=[u"注册",u"注册机"], v=[['n',1],['n',2]])
        new_trie = DoubleArrayTrie.load_dict("./data/test.txt")

        self.assertGreater(trie.exact_match_search(u"注册机"),0)
        self.assertGreater(new_trie.exact_match_search(u"注册机"),0)

    def test_load_big(self):
        trie = DoubleArrayTrie.load(yaya.config.CORE_DICT_NAME)
        self.assertGreater(trie.exact_match_search(u"法兰西斯"),0)

    def test_search(self):
        trie = DoubleArrayTrie.load("./data/test.txt")
        self.assertGreaterEqual(u"一举", 0, u"词典中含有")
        self.assertGreaterEqual(u"一举成名", 0, u"词典中含有")
        self.assertGreaterEqual(u"一举成名天下知", 0, u"词典中含有")
        search = trie.search(u"一举成名天下知", 0)
        while search.next():
            print(search.value)

    def test_searcher(self):
        searcher = DoubleArrayTrie.searcher(u"一举成名天下知", 0)
        while searcher.next():
            print(searcher.begin, searcher.value[0])

    def test_custom_dict(self):
        self.assertGreaterEqual(CustomDict().trie.exact_match_search(u"黄勇"),0)

    def test_max_match(self):
        text = "AABBCD"
        # NRPatternDict.trie.max_match()

class TestAttribute(TestCase):
    def test_total_freq(self):
        text = "测试 n 10 nz 3 p 4"
        attr = Attribute(attr=text)
        self.assertEqual(attr.total_frequency, 17)
        # self.assertEqual(attr.get_nature_frequency('n'), 10)
        self.assertEqual(attr.get_nature_frequency(NATURE.n), 10)
        self.assertEqual(attr.get_nature_frequency(NATURE.nz), 3)
        self.assertEqual(attr.get_nature_frequency(NATURE.p), 4)


class TestAllDict(TestCase):
    def test_PersonDict(self):
        self.assertNotEqual(PersonDict().trie.exact_match_search(u"籍"), -1)




