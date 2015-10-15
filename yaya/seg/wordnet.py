# coding=utf-8
from __future__ import absolute_import
from ..collection.dict import CoreDict
from ..common.nature import NATURE
from ..seg.segment import *
from ..utility.chartype import *

__author__ = 'tony'


class AtomNode:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

    def __str__(self):
        return "AtomNode{ word='%s', nature='%s' }" % (self.word, self.pos)


class Vertex:
    # def __init__(self, real_word, word=None, attribute=None, word_id=0):
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('attribute'):
            attribute = kwargs.get('attribute')
            self.attribute = attribute if isinstance(attribute, Attribute) else Attribute(attribute)
            # self.word = self.attribute.attr[0]
            # self.nature = self.attribute.nature

        self.word_id = kwargs.get('word_id', -1)
        word = kwargs.get('word')
        self.real_word = kwargs.get('real_word')
        self.word = word if word is not None else self.real_word
        self.word_id = kwargs.get('word_id')
        self.vertex_from = None
        self.weight = 0

        self.nature = kwargs.get('nature', None)
        if self.nature is None and self.attribute._nature.__len__() != 0:
            self.nature = self.attribute._nature.items()[0][0]


    def __unicode__(self):
        return self.real_word

    def __str__(self):
        return "%s/%s"%(self.real_word,self.word)

    # @property
    # def nature(self):
    #     if self._nature is not None:
    #         return self._nature
    #     if self.attribute._nature.__len__() != 0:
    #         return self.attribute._nature.items()[0][0]
    #     else:
    #         return None

    def update_from(self, vertex_from):
        weight = vertex_from.weight + Vertex.calc_wight(vertex_from, self)
        if self.vertex_from is None or self.weight > weight:
            self.vertex_from = vertex_from
            self.weight = weight

    @staticmethod
    def calc_wight(vertex_p, vertex_n):
        freq = vertex_p.attribute.total_frequency
        if freq == 0:
            freq = 1
        two_word_freq = CoreBiGramTable().table.get_bifreq(vertex_p.word_id, vertex_n.word_id)
        value = -math.log(SMOOTHING_PARAM * freq / MAX_FREQUENCY + (1 - SMOOTHING_PARAM) *
                          ((1 - SMOOTHING_FACTOR) * two_word_freq / freq + SMOOTHING_FACTOR))
        if value < 0:
            value = -value
        return value


def atom_seg(text, begin, end):
    node_list = []
    offset = begin
    pre_type = get(text[offset])
    offset += 1
    while offset < end:
        cur_type = get(text[offset])
        if cur_type != pre_type:
            # 处理浮点数
            if text[offset] == '.' and pre_type == CT_NUM:
                offset += 1
                while offset < end:
                    cur_type = get(text[offset])
                    if cur_type != CT_NUM:
                        break
                    else:
                        offset += 1
            node_list.append(AtomNode(text[begin:offset], pre_type))
            begin = offset
        pre_type = cur_type
        offset += 1

    if offset == end:
        node_list.append(AtomNode(text[begin:offset], pre_type))

    return node_list


def combine_by_custom_dict(vertex_list):
    word_net = vertex_list
    trie = CustomDict().trie
    for i in range(len(word_net)):
        state = 1
        if word_net[i] is None:
            continue
        state = trie.transition(word_net[i].real_word, state)
        value = None
        if state > 0:
            start = i
            to = i + 1
            end = - 1
            for to in range(to, len(word_net)):
                state = trie.transition(word_net[to].real_word, state)
                if state < 0:
                    break
                output = trie.output(state)
                if output is not None:
                    value = output
                    end = to + 1

            if value is not None:
                word = ""
                for j in range(start, end):
                    word += word_net[j].real_word
                    word_net[j] = None
                word_net[i] = Vertex(real_word=word, attribute=value)

    # todo 考虑加入动态用户词典
    if None in word_net:
        word_net.remove(None)
    return word_net

class WordNet:
    def __init__(self, text=None, vertexs=None):
        self.vertexs = [[]] * (len(text) + 2)
        if vertexs is not None:
            i = 1
            for v in vertexs[1:-1]:
                self.vertexs[i]=[v]
                i += v.real_word.__len__()
            self.vertexs[0] = [vertexs[0]]
            self.vertexs[-1] = [vertexs[-1]]

        else:
            self.vertexs[0] = [new_tag_vertex(TAG_BIGIN)]
            self.vertexs[-1] = [new_tag_vertex(TAG_END)]
        pass

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
                                           attribute=Attribute([atom_node.word, str(nature), '1']),
                                           word_id=-1
                                           ))


def gen_word_net(text, word_net):
    searcher = CoreDict().trie.searcher(text)
    while searcher.next():
        word_net.add(searcher.begin + 1, Vertex(real_word=searcher.value[0],
                                            attribute=searcher.value,
                                            word_id=searcher.index))
    for i in range(word_net.vertexs.__len__()):
    # for i, v in enumerate(word_net.vertexs):
        if word_net.vertexs[i].__len__() == 0:
            j = i + 1
            for j in range(i + 1, word_net.vertexs.__len__() - 1):
                if word_net.vertexs[j].__len__() != 0:
                    break
            word_net.add_atoms(i, atom_seg(text, i - 1, j - 1))
        else:
            i += word_net.vertexs[i][-1].real_word.__len__()


def new_tag_vertex(tag):
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
