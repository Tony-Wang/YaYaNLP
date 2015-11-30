# coding=utf-8
__author__ = 'tony'

from unittest import TestCase

from yaya.recognition import place_recognition
from yaya.collection.dict import CustomDict
from yaya.seg import segment
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex


class TestPlaceRecognition(TestCase):
    def setUp(self):
        self.text = u"蓝翔给宁夏固原市彭阳县红河镇黑牛沟村捐赠了挖掘机"
        self.word_net = WordNet(self.text)
        # 粗分词网
        gen_word_net(self.text, self.word_net)
        # 维特比
        self.vertexs = viterbi(self.word_net.vertexs)
        self.vertexs = segment.combin_by_dict(self.vertexs, CustomDict().trie)
        self.word_net_optimum = WordNet(self.text, vertexs=self.vertexs)

    def test_recognition(self):
        place_recognition.recognition(self.vertexs, self.word_net_optimum, self.word_net)
        vertexs = viterbi(self.word_net_optimum.vertexs)
        self.assertIn(Vertex(u"宁夏", attribute=u"ns 1"), vertexs)
        self.assertIn(Vertex(u"固原市", attribute=u"ns 1"), vertexs)
        self.assertIn(Vertex(u"彭阳县", attribute=u"ns 1"), vertexs)
        self.assertIn(Vertex(u"红河镇", attribute=u"ns 1"), vertexs)
        self.assertIn(Vertex(u"黑牛沟村", attribute=u"ns 1"), vertexs)
