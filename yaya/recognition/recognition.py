# coding=utf-8
from yaya.collection.dict import Searcher
from yaya.seg.viterbi import viterbi, viterbi_template
from yaya.seg.wordnet import Vertex
from yaya.config import Config
__author__ = 'tony'


def role_viterbi(vertexs, wordnet_optimum, hmm, trie, recognition_attr, tag_func, viterbi_fun=viterbi_template):
    tag_list = tag_func(vertexs)
    if Config.debug:
        sb = []
        for i, tag in enumerate(tag_list):
            sb.append(u"[ %s %s ]" % (vertexs[i].real_word, tag))
        print u"角色观察: %s" % u"".join(sb)

    tag_list = viterbi_fun(tag_list, hmm)
    if Config.debug:
        sb = []
        for i, tag in enumerate(tag_list):
            sb.append(u"%s/%s" % (vertexs[i].real_word, tag))
        print(u"角色标注:[%s]" % u", ".join(sb))

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
