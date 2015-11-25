# -*- coding:utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase

from yaya.const import TAG_BIGIN, TAG_END
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex, new_tag_vertex

__author__ = 'tony'


class TestWordNet(TestCase):
    def test_gen_word_net(self):
        text = u"一举成名天下知"
        word_net = WordNet(text)
        gen_word_net(text, word_net)
        self.assertEqual(word_net.vertexs.__len__(), text.__len__() + 2)
        # 一举 一举成名
        # 举
        # 成 成名
        # 名
        # 天 天下
        # 下
        # 知
        self.assertEqual(word_net.vertexs[1].__len__(), 2)
        self.assertEqual(word_net.vertexs[2].__len__(), 1)
        self.assertEqual(word_net.vertexs[3].__len__(), 2)
        self.assertEqual(word_net.vertexs[4].__len__(), 1)
        self.assertEqual(word_net.vertexs[5].__len__(), 2)
        self.assertEqual(word_net.vertexs[6].__len__(), 1)
        self.assertEqual(word_net.vertexs[7].__len__(), 1)

    def test_gen_word_net_include_num(self):
        text = u"123456"
        word_net = WordNet(text)
        gen_word_net(text, word_net)
        self.assertEqual(word_net.vertexs.__len__(), 6 + 2)
        self.assertTrue([] not in word_net.vertexs, u"原始词网，不能可能有空节点")

    def test_vector(self):
        v1 = Vertex(attribute="test nr 1")
        v2 = Vertex(attribute="test nr 1")
        v3 = Vertex(attribute="test nr1 1")
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)
        self.assertIn(v1, [v2])
        self.assertNotIn(v1, [v3])

    def test_tag_vector_real_word_len_should_eq_0(self):
        # 标识词的real_word不能为空，否则在字典里无法表示
        self.assertEqual(new_tag_vertex(TAG_BIGIN).real_word, chr(32))
        self.assertEqual(new_tag_vertex(TAG_END).real_word, chr(32))
