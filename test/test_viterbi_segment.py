# coding=utf-8
from unittest import TestCase

from yaya.seg.segment import vertexs_to_terms
from yaya.seg.viterbi import *
from yaya.seg.wordnet import *

__author__ = 'tony'


class TestViterbiSegment(TestCase):
    def test_viterbi(self):
        text = u"工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
        # text = u"商品23和服务"
        word_net = WordNet(text)
        gen_word_net(text, word_net)
        vertex_list = vertexs_to_terms(viterbi(word_net.vertexs), True)
        self.assertTrue(u"工信处" in vertex_list)
        self.assertTrue(u"女" in vertex_list)
        self.assertTrue(u"干事" in vertex_list)
        self.assertTrue(u"每月" in vertex_list)
        self.assertTrue(u"经过" in vertex_list)
        self.assertTrue(u"下属" in vertex_list)
        self.assertTrue(u"科室" in vertex_list)
        self.assertTrue(u"都" in vertex_list)
        self.assertTrue(u"要" in vertex_list)
        self.assertTrue(u"亲口" in vertex_list)
        self.assertTrue(u"交代" in vertex_list)
        self.assertTrue(u"24" in vertex_list)
        self.assertTrue(u"口" in vertex_list)
        self.assertTrue(u"交换机" in vertex_list)
        self.assertTrue(u"等" in vertex_list)
        self.assertTrue(u"技术性" in vertex_list)
        self.assertTrue(u"器件" in vertex_list)
        self.assertTrue(u"的" in vertex_list)
        self.assertTrue(u"安装" in vertex_list)
        self.assertTrue(u"工作" in vertex_list)

    def test_custom_dict(self):
        text = u"黄勇今天来上班了"
        word_net = WordNet(text)
        gen_word_net(text, word_net)
        vertex_list = viterbi(word_net.vertexs)
        vertex_list = combine_by_custom_dict(vertex_list)
        self.assertEqual(vertex_list[1].real_word, u"黄勇")


class TestViterbi(TestCase):
    def test_computer(self):
        pass
