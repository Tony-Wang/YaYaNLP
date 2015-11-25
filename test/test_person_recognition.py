# coding=utf-8
from unittest import TestCase

from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex
from yaya.recognition.nr import persion_recognition

__author__ = 'tony'


class TestPersonRecognition(TestCase):
    def test_recognition(self):
        text = u"签约仪式前，秦光荣、李纪恒、仇和、王春桂等一同会见了参加签约的企业家。"
        word_net = WordNet(text)
        # 粗分词网
        gen_word_net(text, word_net)
        # 维特比
        vertexs = viterbi(word_net.vertexs)
        word_net_optimum = WordNet(text, vertexs=vertexs)
        vertexs = persion_recognition.recognition(vertexs, word_net_optimum, word_net)
        self.assertIn(Vertex(attribute=u"秦光荣 nr 1"), vertexs)
        self.assertIn(Vertex(attribute=u"李纪恒 nr 1"), vertexs)
        self.assertIn(Vertex(attribute=u"仇和 nr 1"), vertexs)
        self.assertIn(Vertex(attribute=u"王春桂 nr 1"), vertexs)
