# coding=utf-8
from __future__ import absolute_import
import math
import copy

from yaya.collection.dict import *
from yaya.common.nature import NATURE
from yaya.utility.chartype import *
from yaya.collection.bigram import CoreBiGramTable
from yaya.const import *

__author__ = 'tony'


class AtomNode:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

    def __str__(self):
        return "AtomNode{ word='%s', nature='%s' }" % (self.word, self.pos)


class Vertex:
    def __init__(self, real_word, *args, **kwargs):
        if kwargs.has_key('attribute'):
            attribute = kwargs.get('attribute')
        else:
            index, attribute = CoreDict().trie.get(real_word)
        self.attribute = attribute if isinstance(attribute, Attribute) else Attribute(attribute)

        self.word_id = kwargs.get('word_id', -1)
        self.real_word = real_word
        word = kwargs.get('word', None)
        self.word = word if word is not None else self.compile_real_word(self.real_word, self.attribute)
        self.vertex_from = None
        self.weight = 0

    def __unicode__(self):
        return u"%s/%s" % (self.real_word, self.word)

    def __repr__(self):
        return u"Vertex(%(real_word)r, %(attribute)r )" % vars(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.real_word == other.real_word and self.nature == other.nature

    @property
    def nature(self):
        return self.attribute.nature


    @nature.setter
    def nature(self, value):
        self.attribute.nature = value

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

    def compile_real_word(self, real_word, attribute):
        if (len(attribute) >= 1):
            if attribute.nature in [NATURE.nr,
                                    NATURE.nr1,
                                    NATURE.nr2,
                                    NATURE.nrf,
                                    NATURE.nrj]:
                self.word_id = PERSON_WORD_ID
                return TAG_PEOPLE
            elif attribute.nature in [NATURE.ns, NATURE.nsf]:
                self.word_id = PLACE_WORD_ID
                return TAG_PLACE
            elif attribute.nature in [NATURE.nz, NATURE.nx]:
                self.word_id = PROPER_WORD_ID
                return TAG_PROPER
            elif attribute.nature in [
                NATURE.nt,
                NATURE.ntc,
                NATURE.ntcf,
                NATURE.ntcb,
                NATURE.ntch,
                NATURE.nto,
                NATURE.ntu,
                NATURE.nts,
                NATURE.nth,
                NATURE.nit]:
                self.word_id = PLACE_WORD_ID
                return TAG_GROUP
            elif attribute.nature in [NATURE.m, NATURE.mq]:
                self.word_id = NUMBER_WORD_ID
                return TAG_NUMBER
            elif attribute.nature == NATURE.x:
                self.word_id = CLUSTER_WORD_ID
                return TAG_CLUSTER
            elif attribute.nature in [NATURE.t]:
                self.word_id = TIME_WORD_ID
                return TAG_TIME
            return real_word


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


def combine_by_custom_dict(vertexs, dat=CustomDict().trie):
    dat = CustomDict().trie
    for i in range(len(vertexs)):
        state = 1
        if vertexs[i] is None:
            continue
        state = dat.transition(vertexs[i].real_word, state)
        value = None
        if state > 0:
            start = i
            to = i + 1
            end = - 1
            for to in range(to, len(vertexs)):
                state = dat.transition(vertexs[to].real_word, state)
                if state < 0:
                    break
                output = dat.output(state)
                if output is not None:
                    value = output
                    end = to + 1

            if value is not None:
                word = ""
                for j in range(start, end):
                    word += vertexs[j].real_word
                    vertexs[j] = None
                vertexs[i] = Vertex(real_word=word, attribute=value)

    # todo 考虑加入动态用户词典
    return [v for v in vertexs if v is not None]



def dump_vertexs(vertexs):
    logger.info("=" * 30)
    for i, v in enumerate(vertexs):
        logger.info("[%d] %s %s %s" % (i, v.real_word, v.word, v.nature))

class WordNet:
    def __init__(self, text=None, vertexs=None):
        self.vertexs = [[] for i in range(len(text) + 2)]
        self.size = 2
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

    def get_first(self, line):
        if self.vertexs[line].__len__() > 0:
            return self.vertexs[line][0]
        else:
            return None

    def get(self, line, word_length=None):
        if word_length is None:
            return self.vertexs[line]
        for v in self.vertexs[line]:
            if len(v.real_word) == word_length:
                return v
        return None

    def add(self, line, vertex):
        for v in self.vertexs[line]:
            if v.real_word.__len__() == vertex.real_word.__len__():
                return
        if self.vertexs[line].__len__() == 0:
            self.vertexs[line] = [vertex]
        else:
            self.vertexs[line].append(vertex)
        self.size += 1

    def insert(self, line, vertex, word_net):
        self.add(line, vertex)
        # 保证连接性
        for l in range(line - 1, 1, -1):
            if self.get(l, 1) is None:
                first = word_net.get_first(l)
                if first is None:
                    return
                self.vertexs[l].append(copy.deepcopy(first))
                self.size += 1
                if len(self.vertexs) > 1:
                    break
            else:
                break
        l = line + len(vertex.real_word)
        if len(self.get(l)) == 0:
            target_line = word_net.get(l)
            if target_line is None or len(target_line) == 0:
                return
            self.vertexs[l] = copy.deepcopy(target_line)
            self.size += len(self.vertexs[l])

        for l in range(l, len(self.vertexs)):
            if self.get(l).__len__() == 0:
                first = word_net.get_first(l)
                if first is None:
                    break
                self.vertexs[l].append(copy.deepcopy(first))
                self.size += 1
                if self.vertexs[l].__len__() > 1:
                    break
            else:
                break

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
                                           attribute=Attribute([str(nature), '1']),
                                           word_id=-1
                                           ))

    def __len__(self):
        return len(self.vertexs)

    def __unicode__(self):
        sb = []
        sb.append("=" * 30)
        for i, vl in enumerate(self.vertexs):
            sb.append(u"[%d]:%s" % (i, u",".join([unicode(v) for v in vl])))
        sb.append("=" * 30)
        return u"\n".join(sb)

def gen_word_net(text, word_net, dat=CoreDict().trie):
    searcher = dat.buildcoredictsearcher(text)
    while searcher.next():
        word_net.add(searcher.begin + 1, Vertex(real_word=searcher.key,
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
        vertex = Vertex(chr(32), attribute=attribute, word=tag, word_id=word_id)
        return vertex
    else:
        logger.error(u"从核心字典加载%s信息时出错", tag)
        import sys
        sys.exit(-1)
