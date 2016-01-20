# coding=utf-8
from yaya.collection.dict import Attribute, ORG_ATTRIBUTE
from yaya.collection.hmm import OrgTranMatrix
from yaya.common.nature import NATURE
from yaya.common.nt import NT
from yaya.dictionary.org_dict import NTPatternDict, OrgDict
from yaya.recognition.recognition import role_viterbi
from yaya.seg.viterbi import viterbi_standard

__author__ = 'tony'


def recognition(vertexs, wordnet_optimum, wordnet_all):
    # 识别角色，并进行一次维特比
    return role_viterbi(vertexs, wordnet_optimum,
                        hmm=OrgTranMatrix().hmm,
                        trie=NTPatternDict().trie,
                        recognition_attr=ORG_ATTRIBUTE,
                        tag_func=role_tag,
                        viterbi_fun=viterbi_standard
                        )

def role_tag(word_seg_list):
    tag_index_list = []
    for vertex in word_seg_list:
        nature = vertex.nature
        if nature == NATURE.nz:
            if vertex.attribute.total_frequency <= 1000:
                tag_index_list.append(Attribute([str(NT.F), 1000], cls=NT))  # ((NT.F, 1000))
            else:
                break
            continue
        elif nature in [NATURE.ni,
                        NATURE.nic,
                        NATURE.nis,
                        NATURE.nit]:
            tag_index_list.append(Attribute([str(NT.K), 1000, str(NT.D), 1000], cls=NT))
            continue
        elif nature == NATURE.m:
            tag_index_list.append(Attribute([str(NT.M), 1000], cls=NT))
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
