# coding=utf-8
from unittest import TestCase
from yaya.collection.bigram import *

__author__ = 'tony'


class TestBiGramTable(TestCase):
    def test_build(self):
        filename = "./data/test.ngram.txt"
        table = BiGramTable.build(filename)
        self.assertEqual(table.get_bifreq(u"中华", u"鸟类"), 4)
        self.assertEqual(table.get_bifreq(u"中华", u"鸟龙"), 7)

    def test_get_Bifreq(self):
        self.assertEqual(CoreBiGramTable().table.get_bifreq(u"中华", u"鸟类"), 4)
        self.assertEqual(CoreBiGramTable().table.get_bifreq(u"中华", u"鸟龙"), 7)
