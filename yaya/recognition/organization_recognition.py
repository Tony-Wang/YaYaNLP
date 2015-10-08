# coding=utf-8
from yaya.collection.dict import Attribute, Searcher, ORG_ATTRIBUTE
from yaya.collection.hmm import OrgTranMatrix
from yaya.common.nature import NATURE
from yaya.common.nt import NT
from yaya.dictionary.org_dict import NTPatternDict, OrgDict
from yaya.seg.viterbi import viterbi_template, viterbi
from yaya.seg.wordnet import Vertex

__author__ = 'tony'


# def parse_pattern(nrlist, vertexlist, wordnetoptimum, wordnetall):


def recognition(vertexs, wordnet_optimum, wordnet_all):
    # 识别角色，并进行一次维特比
    tag_list = role_tag(vertexs)
    tag_list = viterbi_template(tag_list, OrgTranMatrix().hmm)
    tag_str = [str(x) for x in tag_list]
    tag_str = ''.join(tag_str)
    search = Searcher(NTPatternDict().trie, tag_str)
    vertexs_offset = [0] * len(vertexs)
    offset = 1
    # head tail skip
    for i, v in enumerate(vertexs[1:-1]):
        vertexs_offset[i + 1] = offset
        offset += len(vertexs[i + 1].real_word)

    while search.next():
        name_str = ""
        for i in range(search.begin, search.begin + len(search.value)):
            name_str += vertexs[i].real_word

        # 添加到词网内
        vertex = Vertex(name_str, attribute=ORG_ATTRIBUTE)
        wordnet_optimum.add(vertexs_offset[search.begin], vertex)
    vertexs = viterbi(wordnet_optimum.vertexs)
    return vertexs


def role_tag(word_seg_list):
    tag_index_list = []
    for vertex in word_seg_list:
        nature = vertex.nature
        if nature == NATURE.nz:
            if vertex.attribute.total_frequency <= 1000:
                tag_index_list.append(Attribute([str(NT.F), 1000]), NT)  # ((NT.F, 1000))
            else:
                break
            continue
        elif nature in [NATURE.ni,
                        NATURE.nic,
                        NATURE.nis,
                        NATURE.nit]:
            tag_index_list.append(Attribute([str(NT.K), 1000, str(NT.D), 1000], NT))
            continue
        elif nature == NATURE.m:
            tag_index_list.append((NT.M, 1000))
            continue

        index, value = OrgDict().trie.get(vertex.word)
        if value is None:
            value = Attribute([str(NT.Z), OrgDict().matrix.get_total_freq(NT.Z)], cls=NT)
        # else:
        #     # if not isinstance(value, list):
        #     #     value = value.split()
        #     # value = Attribute(value[1:], cls=NT)

        tag_index_list.append(value)

    return tag_index_list
