# coding=utf-8
from yaya.collection.dict import Searcher
from yaya.seg.viterbi import viterbi, viterbi_template
from yaya.seg.wordnet import Vertex

__author__ = 'tony'


def role_viterbi(vertexs, wordnet_optimum, hmm, trie, recognition_attr, tag_func):
    tag_list = tag_func(vertexs)
    tag_list = viterbi_template(tag_list, hmm)
    tag_str = [str(x) for x in tag_list]
    tag_str = ''.join(tag_str)
    search = Searcher(trie, tag_str)
    vertexs_offset = [0] * len(vertexs)
    offset = 1
    # head tail skip
    for i, v in enumerate(vertexs[1:-1]):
        vertexs_offset[i + 1] = offset
        offset += len(vertexs[i + 1].real_word)
    while search.next():
        name_str = ""
        for i in range(search.begin, search.begin + len(search.key)):
            name_str += vertexs[i].real_word

        # 添加到词网内
        vertex = Vertex(name_str, attribute=recognition_attr)
        wordnet_optimum.add(vertexs_offset[search.begin], vertex)
    vertexs = viterbi(wordnet_optimum.vertexs)
    return vertexs
