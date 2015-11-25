# coding=utf-8
from yaya.collection.dict import Attribute, Searcher
from yaya.collection.hmm import OrgTranMatrix
from yaya.common.nature import NATURE
from yaya.common.nt import NT
from yaya.dictionary.org_dict import NTPatternDict, ORG_WORD_ID, OrgDict
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
    offset = 0
    for i in range(1, len(vertexs) - 2):
        vertexs_offset[i] = offset
        offset += len(vertexs[i].real_word)
    while search.next():
        name_str = ""
        for i in range(search.begin, search.begin + len(search.value)):
            name_str += vertexs[i].real_word

        # 添加到词网内
        vertex = Vertex(attribute=Attribute([name_str, str(NATURE.nt), 1]),
                        word_id=ORG_WORD_ID)
        wordnet_optimum.add(vertexs_offset[search.begin + 1], vertex)
    vertexs = viterbi(wordnet_optimum.vertexs)
    return vertexs


def role_tag(word_seg_list):
    tag_index_list = []
    for vertex in word_seg_list:
        nature = vertex.nature
        if nature == NATURE.nz:
            if vertex.attribute.total_frequency <= 1000:
                tag_index_list.append(Attribute([vertex.real_word, str(NT.F), 1000]), NT)  # ((NT.F, 1000))
            else:
                break
            continue
        elif nature in [NATURE.ni,
                        NATURE.nic,
                        NATURE.nis,
                        NATURE.nit]:
            tag_index_list.append(Attribute([vertex.real_word, str(NT.K), 1000, str(NT.D), 1000], NT))
            continue
        elif nature == NATURE.m:
            tag_index_list.append((NT.M, 1000))
            continue

        index, value = OrgDict().trie.get(vertex.word)
        if value is None:
            value = Attribute([vertex.real_word, str(NT.Z), OrgDict().matrix.get_total_freq(NT.Z)], cls=NT)
        else:
            value = Attribute(value, cls=NT)

        tag_index_list.append(value)

    return tag_index_list
