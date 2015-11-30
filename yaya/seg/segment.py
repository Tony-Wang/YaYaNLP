# coding=utf-8
from collection.dict import CustomDict
from dictionary.chinese_traditional_dict import SimplifiedChineseDict, TraditionalChineseDict
from recognition import place_recognition
from yaya.config import Config
from yaya.recognition import persion_recognition
from yaya.recognition import organization_recognition
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net, Vertex

__author__ = 'tony'


def vertex_to_terms(vertexs):
    terms = []
    offset = 0
    for v in vertexs[1:-1]:
        terms.append((v.real_word, str(v.nature), offset))
        offset += len(v.real_word)
    return terms


def combin_by_dict(vertexs, dat):
    for i, start_v in enumerate(vertexs):
        # skip head and skip combined word
        if i == 0 or start_v is None:
            continue
        state = dat.transition(start_v.real_word, 1)
        if state > 0:
            start = i
            end = -1
            value = None
            for j, end_v in enumerate(vertexs[i + 1:-1]):
                state = dat.transition(end_v.real_word, state)
                if state < 0:
                    break
                value = dat.output(state)
                end = j + 1
            if value is not None:
                for k in range(start, end + i + 1):
                    vertexs[k] = None
                if not isinstance(value, list):
                    value = value.split()
                vertexs[i] = Vertex(value[0], attribute=value[1:])

    return [v for v in vertexs if v is not None]

def seg(text):
    word_net = WordNet(text)
    # 粗分词网
    gen_word_net(text, word_net)
    # 维特比
    vertexs = viterbi(word_net.vertexs)
    if Config.use_custom_dic:
        vertexs = combin_by_dict(vertexs, CustomDict().trie)
    word_net_optimum = WordNet(text, vertexs=vertexs)


    if Config.name_recognize:
        persion_recognition.recognition(vertexs, word_net_optimum, word_net)
    if Config.place_recognize:
        place_recognition.recognition(vertexs, word_net_optimum, word_net)
    vertexs = viterbi(word_net_optimum.vertexs)

    if Config.org_recognize:
        vertexs = organization_recognition.recognition(vertexs, word_net_optimum, word_net)

    return vertex_to_terms(vertexs)


def simplified_to_traditional(text):
    return SimplifiedChineseDict().convert_simplified_to_traditional(text)


def traditional_to_simplified(text):
    return TraditionalChineseDict().convert_traditional_to_simplified(text)
