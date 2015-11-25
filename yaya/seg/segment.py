# coding=utf-8
from yaya.config import Config
from yaya.recognition import persion_recognition
from yaya.seg.viterbi import viterbi
from yaya.seg.wordnet import WordNet, gen_word_net

__author__ = 'tony'


def vertex_to_terms(vertexs):
    terms = []
    offset = 0
    for v in vertexs[1:-1]:
        terms.append((v.real_word, str(v.nature), offset))
        offset += len(v.real_word)
    return terms


def seg(text):
    word_net = WordNet(text)
    # 粗分词网
    gen_word_net(text, word_net)
    # 维特比
    vertexs = viterbi(word_net.vertexs)
    word_net_optimum = WordNet(text, vertexs=vertexs)

    if Config.name_recognize:
        vertexs = persion_recognition.recognition(vertexs, word_net_optimum, word_net)

    return vertex_to_terms(vertexs)
