from yaya.collection.dict import Attribute
from yaya.common.nature import NATURE
from yaya.common.nr import NR
from yaya.dictionary.person_dict import PersonDict, NRPatternDict

__author__ = 'tony'


def recognition(word_seg_list, wordnet_optimum, wordnet_all):
    role_tag_list = role_tag(word_seg_list)


def role_tag(word_seg_list):
    tag_index_list = []
    for vertex in word_seg_list:
        if vertex.nature == NATURE.nr.index and vertex.attribute.total_frequency <= 1000:
            if vertex.real_word.__len__() == 2:
                tag_index_list.append(((NR.x, 1), (NR.G, 1)))
                continue
        index, value = PersonDict().trie.get(vertex.real_word)
        if value is None:
            value = Attribute([vertex.real_word, str(NR.A), PersonDict().matrix.get_total_freq(NR.A)], cls=NR)
        else:
            value = Attribute(value, cls=NR)

        tag_index_list.append(value)

    return tag_index_list


def parse_pattern(nrlist, vertexlist, wordnetoptimum, wordnetall):
    pass