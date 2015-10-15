# coding=utf-8
from unittest import TestCase
from yaya.seg.wordnet import atom_seg
from yaya.utility.chartype import *

__author__ = 'tony'


class TestSegment(TestCase):
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
