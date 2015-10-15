# coding=utf-8
from unittest import TestCase
from yaya.seg.viterbi import *
from yaya.seg.wordnet import *

__author__ = 'tony'


class TestViterbiSegment(TestCase):
    def test_viterbi(self):
        text = u"工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
        # text = u"商品23和服务"
        word_net = WordNet(text)
        gen_word_net(text, word_net)
        vertex_list = viterbi(word_net.vertexs)
        self.assertEqual(vertex_list[1].__unicode__(), u"工信处")
        self.assertEqual(vertex_list[2].__unicode__(), u"女")
        self.assertEqual(vertex_list[3].__unicode__(), u"干事")
        self.assertEqual(vertex_list[4].__unicode__(), u"每月")
        self.assertEqual(vertex_list[5].__unicode__(), u"经过")
        self.assertEqual(vertex_list[6].__unicode__(), u"下属")
        self.assertEqual(vertex_list[7].__unicode__(), u"科室")
        self.assertEqual(vertex_list[8].__unicode__(), u"都")
        self.assertEqual(vertex_list[9].__unicode__(), u"要")
        self.assertEqual(vertex_list[10].__unicode__(), u"亲口")
        self.assertEqual(vertex_list[11].__unicode__(), u"交代")
        self.assertEqual(vertex_list[12].__unicode__(), u"24")
        self.assertEqual(vertex_list[13].__unicode__(), u"口")
        self.assertEqual(vertex_list[14].__unicode__(), u"交换机")
        self.assertEqual(vertex_list[15].__unicode__(), u"等")
        self.assertEqual(vertex_list[16].__unicode__(), u"技术性")
        self.assertEqual(vertex_list[17].__unicode__(), u"器件")
        self.assertEqual(vertex_list[18].__unicode__(), u"的")
        self.assertEqual(vertex_list[19].__unicode__(), u"安装")
        self.assertEqual(vertex_list[20].__unicode__(), u"工作")

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
