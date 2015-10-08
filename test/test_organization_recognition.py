# coding=utf-8
__author__ = 'tony'
from unittest import TestCase
from yaya.recognition import person_recognition
from yaya.recognition import place_recognition
from yaya.recognition import organization_recognition
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, Vertex, gen_word_net, dump_vertexs


class TestOrgRecognition(TestCase):
    def setUp(self):
        self.text = u"济南杨铭宇餐饮管理有限公司是由杨先生创办的餐饮企业"
        self.word_net = WordNet(self.text)
        # 粗分词网
        gen_word_net(self.text, self.word_net)
        # 维特比
        self.vertexs = viterbi(self.word_net.vertexs)
        self.word_net_optimum = WordNet(self.text, vertexs=self.vertexs)

    def test_recognition_1_level(self):
        # vertexs = persion_recognition.recognition(vertexs, word_net_optimum, word_net)
        # word_net_optimum = WordNet(text, vertexs=vertexs)
        organization_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        vertexs = viterbi(self.word_net_optimum.vertexs)
        self.assertIn(Vertex(u"济南杨铭宇餐饮管理有限公司", attribute=u"nt 1"), vertexs)

    def test_recognition_2_level(self):
        person_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        place_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        word_net_optimum = WordNet(self.text, vertexs=self.vertexs)
        organization_recognition.recognition(self.vertexs, word_net_optimum, self.word_net)
        vertexs = viterbi(word_net_optimum.vertexs)
        dump_vertexs(vertexs)
        self.assertIn(Vertex(u"济南杨铭宇餐饮管理有限公司", attribute=u"nt 1"), vertexs)
