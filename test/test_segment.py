# coding=utf-8
from unittest import TestCase

from yaya.seg import segment
from yaya.seg.wordnet import atom_seg
from yaya.utility.chartype import *

__author__ = 'tony'


class TestAtomSegment(TestCase):
    def test_char_type(self):
        self.assertEqual(get('a'), CT_SINGLE)
        self.assertEqual(get('1'), CT_NUM)
        self.assertEqual(get(u'中'), CT_CHINESE)

    def test_atom_seg(self):
        text = '12341'
        node_list = atom_seg(text, 0, text.__len__())
        self.assertEqual(node_list.__len__(), 1)
        self.assertEqual(node_list[0].pos, CT_NUM)
        text = '123.41'
        node_list = atom_seg(text, 0, text.__len__())
        self.assertEqual(node_list.__len__(), 1)
        self.assertEqual(node_list[0].pos, CT_NUM)
        text = 'abc'
        node_list = atom_seg(text, 0, text.__len__())
        self.assertEqual(node_list.__len__(), 1)
        self.assertEqual(node_list[0].pos, CT_SINGLE)


class TestSegment(TestCase):
    def test_seg_find_nr(self):
        text = u"签约仪式前，秦光荣、李纪恒、仇和、王春桂等一同会见了参加签约的企业家。"
        terms = segment.seg(text)
        self.assertIn((u"秦光荣", 'nr', 6), terms, u"测试是否找出人名")
        self.assertIn((u"李纪恒", 'nr', 10), terms, u"测试是否找出人名")
        self.assertIn((u"仇和", 'nr', 14), terms, u"测试是否找出人名")
        self.assertIn((u"王春桂", 'nr', 17), terms, u"测试是否找出人名")
