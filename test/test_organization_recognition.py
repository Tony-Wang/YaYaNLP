# coding=utf-8
from yaya.recognition.nt import organization_recognition

__author__ = 'tony'
# coding=utf-8
from unittest import TestCase
from yaya.seg import segment
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex

__author__ = 'tony'


class TestOrgRecognition(TestCase):
    def setUp(self):
        self.text = u"济南杨铭宇餐饮管理有限公司是由杨先生创办的餐饮企业"
        self.vertexs = segment.seg(self.text)
        self.word_net = WordNet(self.text)
        # 粗分词网
        gen_word_net(self.text, self.word_net)
        # 维特比
        self.vertexs = viterbi(self.word_net.vertexs)
        self.word_net_optimum = WordNet(self.text, vertexs=self.vertexs)

    def test_recognition_1_level(self):
        # vertexs = persion_recognition.recognition(vertexs, word_net_optimum, word_net)
        # word_net_optimum = WordNet(text, vertexs=vertexs)
        vertexs = organization_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        self.assertIn(Vertex(attribute=u"铭宇餐饮管理有限公司 nt 1"), vertexs)

        # def test_recognition_2_level(self):
        #     vertexs = persion_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        #     word_net_optimum = WordNet(self.text, vertexs=vertexs)
        #
        #     vertexs = organization_recognition.recognition(vertexs, word_net_optimum, self.word_net)
        #     self.assertIn(Vertex(attribute=u"铭宇餐饮管理有限公司 nt 1"), vertexs)
