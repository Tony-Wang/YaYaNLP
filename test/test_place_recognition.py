# coding=utf-8
from yaya.recognition import place_recognition

__author__ = 'tony'
# coding=utf-8
from unittest import TestCase
from yaya.seg import segment
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex

__author__ = 'tony'


class TestPlaceRecognition(TestCase):
    def setUp(self):
        self.text = u"江苏省南京市栖霞区"
        self.vertexs = segment.seg(self.text)
        self.word_net = WordNet(self.text)
        # 粗分词网
        gen_word_net(self.text, self.word_net)
        # 维特比
        self.vertexs = viterbi(self.word_net.vertexs)
        self.word_net_optimum = WordNet(self.text, vertexs=self.vertexs)

    def test_recognition_1_level(self):
        vertexs = place_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        self.assertIn(Vertex(attribute=u"铭宇餐饮管理有限公司 ns 1"), vertexs)
