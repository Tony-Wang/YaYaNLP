# coding=utf-8
import math
from ..utility.chartype import *
from ..collection.dict import CustomDict
from ..collection.dict import Attribute
from ..collection.bigram import CoreBiGramTable
from ..const import *

__author__ = 'tony'


class AtomNode:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

    def __str__(self):
        return "AtomNode{ word='%s', nature='%s' }" % (self.word, self.pos)


class Vertex:
    def __init__(self, real_word, word=None, attribute=None, word_id=0):
        self.word_id = word_id
        self.word = word if word is not None else real_word
        self.real_word = real_word
        self.attribute = attribute if isinstance(attribute, Attribute) else Attribute(attribute)
        self.vertex_from = None
        self.weight = 0

    def __unicode__(self):
        return self.real_word

    @property
    def nature(self):
        if self.attribute.nature.__len__() == 1:
            return self.nature[0][0]
        else:
            return None

    def update_from(self, vertex_from):
        weight = vertex_from.weight + Vertex.calc_wight(vertex_from, self)
        if self.vertex_from is None or self.weight > weight:
            self.vertex_from = vertex_from
            self.weight = weight

    @staticmethod
    def calc_wight(vertex_p, vertex_n):
        freq = vertex_p.attribute.total_frequency()
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
