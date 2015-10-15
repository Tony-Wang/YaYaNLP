# coding=utf-8
from unittest import TestCase
from yaya.collection.dict import Attribute, DoubleArrayTrie, Searcher
from yaya.collection.hmm import PersonTranMatrix
from yaya.common.nature import NATURE
from yaya.common.nr import NR, NRPattern
from yaya.const import *
from yaya.dictionary.person_dict import NRPatternDict, PersonDict, PERSON_ATTRIBUTE, PERSON_WORD_ID
from yaya.recognition.nr.persion_recognition import role_tag
from yaya.seg.viterbi import viterbi_roletag, viterbi, viterbi_template
from yaya.seg.wordnet import WordNet, gen_word_net, new_tag_vertex, Vertex

__author__ = 'tony'


class TestRole_tag(TestCase):
    def test_role_tag(self):
        word_seg_list = [
            new_tag_vertex(TAG_BIGIN),
            Vertex(real_word=u'王', attribute=Attribute('秦 n 1')),
            Vertex(real_word=u'光荣', attribute=Attribute('光荣 n 1')),
            Vertex(real_word=u'同志', attribute=Attribute('同志 n 1')),
            new_tag_vertex(TAG_END),
        ]
        taglist = role_tag(word_seg_list)

        self.assertTrue(isinstance(taglist, list))
        self.assertEqual(taglist[2].to_tuple(), (u'光荣', u'Z', u'29', u'L', u'2'))

        tag_index_list = viterbi_roletag(taglist, PersonTranMatrix().hmm)
        self.assertEqual(tag_index_list[0], NR.A)
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


    def test_NRPattern_Search(self):
        text = u"签约仪式前，秦光荣、李纪恒、仇和、王春桂等一同会见了参加签约的企业家。"
        word_net = WordNet(text)
        # 粗分词网
        gen_word_net(text, word_net)

        # 维特比
        vertexs = viterbi(word_net.vertexs)

        # 识别角色，并进行一次维特比
        tag_list = viterbi_template(role_tag(vertexs), PersonTranMatrix().hmm)
        tag_str = [str(x) for x in tag_list]
        tag_str = ''.join(tag_str)
        self.assertEqual(len(vertexs), len(tag_str), u"标签序列应该和顶点序列等长")
        search = Searcher(NRPatternDict().trie, tag_str)
        print(tag_str)

        word_net_optimum = WordNet(text, vertexs=vertexs)

        vertexs_offset = [0]*len(vertexs)
        offset = 0
        for i in range(len(vertexs)):
            vertexs_offset[i] = offset
            offset += len(vertexs[i].real_word)

        while search.next():
            name_str = ""
            for i in range(search.begin, search.begin+len(search.value)):
                name_str += vertexs[i].real_word

            # 添加到词网内
            word_net_optimum.add(vertexs_offset[search.begin], Vertex(word=TAG_PEOPLE,
                                                      real_word=name_str,
                                                      word_id=PERSON_WORD_ID,
                                                      nature=NATURE.nr,
                                                      attribute=PERSON_ATTRIBUTE))

        vertexs = viterbi(word_net_optimum.vertexs)

        # todo: 对词性使用HMM 选择。
        for v in vertexs:
            print v.real_word, v.nature





