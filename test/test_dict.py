# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from yaya.collection.dict import *
import yaya.config
from yaya.dictionary.person_dict import PersonDict

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
        # trie.dump()
        # self.assertGreaterEqual(trie.exactMatchSearch(u"一举"),0)
        self.assertGreater(trie.exact_match_search(u"一举一动"),0)
        self.assertGreater(trie.exact_match_search(u"阿拉伯"),0)
        self.assertGreater(trie.exact_match_search(u"阿拉伯人"),0)

    # def test_save_load(self):
    #     trie = DoubleArrayTrie()
    #     words = []
    #     words.append("一举")
    #     words.append("一举一动")
    #     words.append("一举成名")
    #     words.append("一举成名天下知")
    #     words.append("啊")
    #     words.append("埃及")
    #     words.append("阿拉伯")
    #     words.append("阿拉伯人")
    #     words.append("阿根廷")
    #     words.append("阿胶")
    #     words.append("法兰西斯")
    #     words.sort()
    #
    #     trie.build(words)
    #     print(trie.base[42])
    #     filename="./data/test.txt.ya"
    #     DoubleArrayTrie.save_bin(trie,filename)
    #     print(trie.base[42])
    #     new_trie = DoubleArrayTrie.load_bin(filename)
    #     print(new_trie.base[42])
    #     self.assertEqual(trie.base.__len__(), new_trie.base.__len__())
    #     self.assertListEqual(trie.check, new_trie.check)
    #     self.assertListEqual(trie.base, new_trie.base)
    #     self.assertGreaterEqual(trie.exact_match_search(u"一举"),0)
    #     self.assertGreaterEqual(trie.exact_match_search(u"法兰西斯"),0)
    #     self.assertGreaterEqual(new_trie.exact_match_search(u"一举"),0)
    #     self.assertGreaterEqual(new_trie.exact_match_search(u"法兰西斯"),0)

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

class TestAttribute(TestCase):
    def test_total_freq(self):
        text = "测试 n 10 nz 3 p 4"
        attr = Attribute(attr=text)
        self.assertEqual(attr.total_frequency, 17)
        self.assertEqual(attr.get_nature_frequency('n'), 10)
        self.assertEqual(attr.get_nature_frequency('nz'), 3)
        self.assertEqual(attr.get_nature_frequency('p'), 4)


class TestAllDict(TestCase):
    def test_PersonDict(self):
        self.assertNotEqual(PersonDict().trie.exact_match_search(u"籍"), -1)




