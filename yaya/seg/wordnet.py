# coding=utf-8
from __future__ import absolute_import
from ..collection.dict import CoreDict
from ..common.nature import NATURE
from ..seg.segment import *
from ..utility.chartype import *

__author__ = 'tony'


class WordNet:
    def __init__(self, text):
        self.text = text
        self.vertexs = [[]] * (len(text) + 2)
        self.vertexs[0] = [WordNet.new_tag_node(TAG_BIGIN)]
        self.vertexs[-1] = [WordNet.new_tag_node(TAG_END)]
        pass

    @staticmethod
    def new_tag_node(tag):
        word_id, attribute = CoreDict().trie.get(tag)
        if word_id > 0:
            return Vertex(word=tag,
                          real_word=chr(32),
                          attribute=attribute,
                          word_id=word_id)
        else:
            logger.error(u"从核心字典加载%s信息时出错", tag)
            import sys
            sys.exit(-1)

    def add(self, line, vertex):
        for v in self.vertexs[line]:
            if v.real_word.__len__() == vertex.real_word.__len__():
                return
        if self.vertexs[line].__len__() == 0:
            self.vertexs[line] = [vertex]
        else:
            self.vertexs[line].append(vertex)

    def add_atoms(self, line, atom_list):
        offset = 0
        for atom_node in atom_list:
            word = atom_node.word
            nature = NATURE.n
            if atom_node.pos in [CT_INDEX, CT_NUM]:
                nature = NATURE.m
                word = TAG_NUMBER
            elif atom_node.pos in [CT_DELIMITER]:
                nature = NATURE.w
            elif atom_node.pos in [CT_LETTER, CT_SINGLE]:
                nature = NATURE.nx
                word = TAG_CLUSTER
            self.add(line + offset, Vertex(word=word,
                                           real_word=atom_node.word,
                                           attribute=Attribute([atom_node.word, nature, '1'])
                                           ))

    def gen_word_net(self):
        searcher = CoreDict().trie.searcher(self.text)
        while searcher.next():
            self.add(searcher.begin + 1, Vertex(real_word=searcher.value[0],
                                                attribute=searcher.value,
                                                word_id=searcher.index))
        for i in range(self.vertexs.__len__()):
            if self.vertexs[i].__len__() == 0:
                j = i + 1
                for j in range(i + 1, self.vertexs.__len__() - 1):
                    if self.vertexs[j].__len__() != 0:
                        break
                self.add_atoms(i, atom_seg(self.text, i - 1, j - 1))
                i = j
            else:
                i += self.vertexs[i][-1].real_word.__len__()
