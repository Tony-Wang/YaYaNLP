# coding=utf-8
from unittest import TestCase

from yaya.collection.dict import DoubleArrayTrie
from yaya.seg import segment
from yaya.seg.wordnet import atom_seg, WordNet, gen_word_net, combine_by_custom_dict
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

    def test_combin_by_dict(self):
        dat = DoubleArrayTrie()
        dat.build([u"江", u"河", u"湖", "海"])
        text = u"江河湖海"
        word_net = WordNet(text)
        gen_word_net(text, word_net, dat)
        vertexs = [v[0] for v in word_net.vertexs]
        self.assertEqual(len(word_net), 6, u"自定义字典分词")

        combin_dat = DoubleArrayTrie()
        combin_dat.build(key=[u"江河湖海"], v=[u"江河湖海 n 1"])
        vertexs = combine_by_custom_dict(vertexs, combin_dat)
        self.assertEqual(len(vertexs), 3, u"合并完成后应该只有前尾加中间词")
