__author__ = 'tony'
# coding=utf-8
from yaya.collection.dict import Attribute, Searcher
from yaya.collection.hmm import PersonTranMatrix
from yaya.common.nature import NATURE
from yaya.common.nr import NR
from yaya.dictionary.person_dict import PersonDict, NRPatternDict, PERSON_WORD_ID
from yaya.seg.viterbi import viterbi_template, viterbi
from yaya.seg.wordnet import Vertex

__author__ = 'tony'


# def parse_pattern(nrlist, vertexlist, wordnetoptimum, wordnetall):
def recognition(vertexs, wordnet_optimum, wordnet_all):
    # 识别角色，并进行一次维特比
    tag_list = viterbi_template(role_tag(vertexs), PersonTranMatrix().hmm)
    tag_str = [str(x) for x in tag_list]
    tag_str = ''.join(tag_str)
    search = Searcher(NRPatternDict().trie, tag_str)
    vertexs_offset = [0] * len(vertexs)
    offset = 0
    for i in range(1, len(vertexs) - 2):
        vertexs_offset[i] = offset
        offset += len(vertexs[i].real_word)
    while search.next():
        name_str = ""
        for i in range(search.begin, search.begin + len(search.value)):
            name_str += vertexs[i].real_word

        # 添加到词网内
        vertex = Vertex(attribute="%s %s 1" % (name_str, 'nr'),
                        word_id=PERSON_WORD_ID)
        wordnet_optimum.add(vertexs_offset[search.begin + 1], vertex)
    vertexs = viterbi(wordnet_optimum.vertexs)
    return vertexs


def role_tag(word_seg_list):
    tag_index_list = []
    for vertex in word_seg_list:
        if vertex.nature == NATURE.nr.index and vertex.attribute.total_frequency <= 1000:
            if vertex.real_word.__len__() == 2:
                tag_index_list.append(Attribute("%s %s 1 %s 1" % (vertex.real_word, NR.X, NR.G), NR))
                continue
        index, value = PersonDict().trie.get(vertex.real_word)
        if value is None:
            value = Attribute([vertex.real_word, str(NR.A), PersonDict().matrix.get_total_freq(NR.A)], cls=NR)
        else:
            value = Attribute(value, cls=NR)
        tag_index_list.append(value)
    return tag_index_list
