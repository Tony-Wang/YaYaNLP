# coding=utf-8
from unittest import TestCase
from yaya.collection.hmm import PersonTranMatrix

__author__ = 'tony'


class TestHMMMatrix(TestCase):
    def test_load(self):
        self.assertIsNotNone(PersonTranMatrix().hmm, u"加载人名识别HMM转换矩阵")
        self.assertNotEqual(PersonTranMatrix().hmm.matrix.__len__(), 0)
        self.assertEqual(PersonTranMatrix().hmm.total_freq, 43938702)
