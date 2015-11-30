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
        trie.build(key=words, v=['一', '一', '一', '一', '二', '三', '四', '四', '四', '四'])
        self.assertGreater(trie.exact_match_search(u"一举一动"), 0)
        self.assertGreater(trie.exact_match_search(u"阿拉伯"), 0)
        self.assertGreater(trie.exact_match_search(u"阿拉伯人"), 0)

    def test_load_dict(self):
        trie = DoubleArrayTrie()
        trie.build(key=[u"注册", u"注册机"], v=[['n', 1], ['n', 2]])
        new_trie = DoubleArrayTrie.load_dict("./data/test.txt")

        self.assertGreater(trie.exact_match_search(u"注册机"), 0)
        self.assertGreater(new_trie.exact_match_search(u"注册机"), 0)

    def test_load_big(self):
        trie = DoubleArrayTrie.load(yaya.config.CORE_DICT_NAME)
        self.assertGreater(trie.exact_match_search(u"法兰西斯"), 0)

    def test_search(self):
        trie = DoubleArrayTrie.load("./data/test.txt")
        self.assertGreaterEqual(u"一举", 0, u"词典中含有")
        self.assertGreaterEqual(u"一举成名", 0, u"词典中含有")
        self.assertGreaterEqual(u"一举成名天下知", 0, u"词典中含有")
        search = trie.search(u"一举成名天下知", 0)
        while search.next():
            print(search.value)

    def test_searcher_generator(self):
        trie = DoubleArrayTrie.load("./data/test.txt")
        self.assertGreaterEqual(u"一举", 0, u"词典中含有")
        self.assertGreaterEqual(u"一举成名", 0, u"词典中含有")
        self.assertGreaterEqual(u"一举成名天下知", 0, u"词典中含有")
        search = trie.search(u"一举成名天下知", 0)
        terms = []
        for i, k, v in search.search_all_words():
            terms.append((i, k, v))
        self.assertEqual(len(terms), 5, u"搜索生成器，查找出所有词典里有的词")

    # def test_searcher(self):
    #     searcher = DoubleArrayTrie.buildcoredictsearcher(u"红河镇", 0)
    #     result = [ x for x in searcher.search_all_words()]
    #     self.assertIn(u"红河镇", result)

    def test_custom_dict(self):
        self.assertGreaterEqual(CustomDict().trie.exact_match_search(u"黄勇"), 0)

    def test_dat_transition(self):
        trie = DoubleArrayTrie.load("./data/test.txt")
        self.assertNotEqual(trie.transition(u"法兰西", 1), -1)
        self.assertEqual(trie.transition(u"法兰东", 1), -1)
        p = trie.transition(u"法兰", 1)
        self.assertNotEqual(trie.transition(u"西", p), -1)
        self.assertEqual(trie.transition(u"东", p), -1)

    def test_dat_output(self):
        dat = DoubleArrayTrie()
        dat.build(key=[u"江河湖海"], v=[u"江河湖海 n 1"])
        state = dat.transition(u'江河湖海', 1)
        self.assertGreater(state, -1)
        self.assertIsNotNone(dat.output(state))
        self.assertEqual(dat.output(state), dat.get(u"江河湖海")[1])

        # state = CoreDict().trie.transition(u"大海", 1)
        # self.assertGreater(state, -1)
        # self.assertEqual(CoreDict().trie.output(state), CoreDict().trie.get(u'大海')[1])



class TestAttribute(TestCase):
    def test_total_freq(self):
        text = "测试 n 10 nz 3 p 4"
        attr = Attribute(attr=text.split()[1:])
        self.assertEqual(attr.total_frequency, 17)
        # self.assertEqual(attr.get_nature_frequency('n'), 10)
        self.assertEqual(attr.get_nature_frequency(NATURE.n), 10)
        self.assertEqual(attr.get_nature_frequency(NATURE.nz), 3)
        self.assertEqual(attr.get_nature_frequency(NATURE.p), 4)


class TestAllDict(TestCase):
    def test_PersonDict(self):
        self.assertNotEqual(PersonDict().trie.exact_match_search(u"籍"), -1)
