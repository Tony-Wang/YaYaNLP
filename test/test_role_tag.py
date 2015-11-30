# coding=utf-8
from unittest import TestCase

from yaya.collection.dict import Attribute, DoubleArrayTrie
from yaya.collection.hmm import PersonTranMatrix
from yaya.common.nr import NR, NRPattern
from yaya.const import *
from yaya.recognition.persion_recognition import role_tag
from yaya.seg.viterbi import viterbi_roletag
from yaya.seg.wordnet import new_tag_vertex, Vertex

__author__ = 'tony'


class TestRole_tag(TestCase):
    def test_role_tag(self):
        word_seg_list = [
            new_tag_vertex(TAG_BIGIN),
            Vertex(u"秦", attribute=Attribute(u'n 1')),
            Vertex(u"光荣", attribute=Attribute(u'n 1')),
            Vertex(u"同志", attribute=Attribute(u'n 1')),
            new_tag_vertex(TAG_END),
        ]
        taglist = role_tag(word_seg_list)

        self.assertTrue(isinstance(taglist, list))
        self.assertEqual(taglist[2].to_tuple(), (u'Z', u'29', u'L', u'2'))

        tag_index_list = viterbi_roletag(taglist, PersonTranMatrix().hmm)
        self.assertEqual(tag_index_list[0], NR.A, u"人名识别，第一个标识应该为TAG_BAGIN")
        self.assertEqual(tag_index_list[1], NR.B)
        self.assertEqual(tag_index_list[2], NR.Z)
        self.assertEqual(tag_index_list[3], NR.L)
        self.assertEqual(tag_index_list[4], NR.A)

    def test_NRPattern(self):
        """


        """
        trie = DoubleArrayTrie()
        NRPattern.sort()
        trie.build(key=NRPattern)
        self.assertTrue(trie.exact_match_search("BCD") != -1)
        self.assertTrue(trie.exact_match_search("BBCD") != -1)
        self.assertTrue(trie.exact_match_search("BG") != -1)
        self.assertTrue(trie.exact_match_search("DG") != -1)
        self.assertTrue(trie.exact_match_search("CD") == -1)










