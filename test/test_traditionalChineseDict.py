# coding=utf-8
from unittest import TestCase

import config
from dictionary.chinese_traditional_dict import TraditionalChineseDict, SimplifiedChineseDict

__author__ = 'tony'


class TestTraditionalChineseDict(TestCase):
    def test_convert_simplified_to_traditional(self):
        simplified = TraditionalChineseDict().convert_traditional_to_simplified(u"用筆記簿型電腦寫程式HelloWorld")
        self.assertEqual(simplified, u"用笔记本电脑写程序HelloWorld")

    def test_convert_traditional_to_simplified(self):
        config.Config.debug = True
        traditional = SimplifiedChineseDict().convert_simplified_to_traditional(u"用笔记本电脑写程序HelloWorld")
        self.assertEqual(traditional, u"用筆記簿型電腦寫程式HelloWorld")

    def test_traditional_chinese_dict_search_all_words(self):
        searcher = TraditionalChineseDict().trie.search(u"用筆記簿型電腦寫程式HelloWorld")
        for i, k, v in searcher.search_all_words():
            print i, k, v
