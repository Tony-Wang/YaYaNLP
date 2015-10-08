from yaya.collection.dict import Attribute
from yaya.common.nature import NATURE
from yaya.common.nr import NR
from yaya.dictionary.person_dict import PersonDict

__author__ = 'tony'


def recognition(word_seg_list, wordnet_optimum, wordnet_all):
    role_tag_list = role_tag(word_seg_list)


def role_tag(word_seg_list):
    tag_list = []
    for vertex in word_seg_list:
        if vertex.nature == NATURE.nr.index and vertex.attribute.total_frequency <= 1000:
            if vertex.real_word.__len__() == 2:
                tag_list.append(((NR.x, 1), (NR.G, 1)))
                continue
    value = PersonDict().trie.get(vertex.real_word)
    if value is None:
        value = (NR.A, PersonDict().matrix.get_total_freq(NR.A.index))
    else:
        value = Attribute.to_tuple(value)
