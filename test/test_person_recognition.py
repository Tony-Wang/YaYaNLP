# coding=utf-8
from unittest import TestCase

from yaya.seg import segment
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex
from yaya.recognition import person_recognition

__author__ = 'tony'


class TestPersonRecognition(TestCase):
    def test_recognition(self):
        text = u"签约仪式前，秦光荣、李纪恒、仇和、王春桂、张晓辉等一同会见了参加签约的企业家。"
        word_net = WordNet(text)

        # 粗分词网
        gen_word_net(text, word_net)

        # 维特比
        vertexs = viterbi(word_net.vertexs)
        word_net_optimum = WordNet(text, vertexs=vertexs)
        person_recognition.recognition(vertexs, word_net_optimum, word_net)
        vertexs = viterbi(word_net_optimum.vertexs)
        self.assertIn(Vertex(u"秦光荣", attribute=u"nr 1"), vertexs)
        self.assertIn(Vertex(u"李纪恒", attribute=u"nr 1"), vertexs)
        self.assertIn(Vertex(u"仇和", attribute=u"nr 1"), vertexs)
        self.assertIn(Vertex(u"王春桂", attribute=u"nr 1"), vertexs)
        self.assertIn(Vertex(u"张晓辉", attribute=u"nr 1"), vertexs)
        print(vertexs)

    def test_person_name_V_should_split_to_EL_DL(self):
        text = u"龚学平、张晓辉等领导说,邓颖超生前杜绝超生"
        vertexs = segment.seg_to_vertexs(text)
        terms = segment.vertexs_to_terms(vertexs, True)
        self.assertIn(u"龚学平", terms)
        self.assertIn(u"张晓辉", terms)
        self.assertIn(u"邓颖超", terms)

