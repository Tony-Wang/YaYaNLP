# coding=utf-8
from yaya.common.ns import NS
from yaya.dictionary.place_dict import NSPatternDict, PlaceDict

__author__ = 'tony'
# coding=utf-8
from yaya.collection.dict import Attribute, Searcher
from yaya.collection.hmm import PlaceTranMatrix
from yaya.common.nature import NATURE
from yaya.seg.viterbi import viterbi_template
from yaya.seg.wordnet import Vertex

__author__ = 'tony'


def recognition(vertexs, wordnet_optimum, wordnet_all):
    # 识别角色，并进行一次维特比
    tag_list = viterbi_template(role_tag(vertexs), PlaceTranMatrix().hmm)
    tag_str = [str(x) for x in tag_list]
    tag_str = ''.join(tag_str)
    search = Searcher(NSPatternDict().trie, tag_str)
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
        vertex = Vertex(name_str, attribute="ns 1")
        wordnet_optimum.insert(vertexs_offset[search.begin + 1], vertex, wordnet_all)


def role_tag(word_seg_list):
    tag_index_list = []
    for vertex in word_seg_list:
        if vertex.nature == NATURE.ns.index and vertex.attribute.total_frequency <= 1000:
            if vertex.real_word.__len__() < 3:
                tag_index_list.append(Attribute("%s 1 %s 1" % (NS.H, NS.G), NS))
                continue
        index, value = PlaceDict().trie.get(vertex.real_word)
        if value is None:
            value = Attribute([str(NS.Z), PlaceDict().matrix.get_total_freq(NS.Z)], cls=NS)
        # else:
        #     if not isinstance(value, list):
        #         value = value.split()
        #     value = Attribute(value[1:], cls=NS)
        tag_index_list.append(value)
    return tag_index_list
