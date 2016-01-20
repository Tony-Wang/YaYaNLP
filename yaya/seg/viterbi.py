# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
import math

from yaya.const import DOUBLE_MAX
from yaya.config import Config

__author__ = 'tony'


class Viterbi:
    @staticmethod
    def computer(obs, states, start_p, trans_p, emit_p):
        max_states_value = 0
        for s in states:
            max_states_value = max(max_states_value, s)
        max_states_value += 1

        V = [[0 for col in range(obs.__len__())] for row in range(max_states_value)]
        path = [[0 for col in range(max_states_value)] for row in range(obs.__len__())]

        for y in states:
            V[0][y] = start_p[y] + emit_p[obs[0]]
            path[y][0] = y

        for t in range(obs.__len__()):
            new_path = [[0 for col in range(max_states_value) for row in range(obs.__len__())]]
            for y in states:
                prob = DOUBLE_MAX
                states = 0
                for y0 in states:
                    nprob = V[t - 1][y0] + trans_p[y0][y] + emit_p[y][obs[t]]
                    if nprob < prob:
                        prob = nprob
                        state = y0
                        V[t][y] = prob
                        path[state][0:t] = new_path[y][0:t]
                        new_path[y][t] = y
            path = new_path
        prob = DOUBLE_MAX
        state = 0
        for y in states:
            if V[-1][y] < prob:
                prob = V[-1][y]
                state = y
        return path[state]


def viterbi(vertexs):
    for v in vertexs[1]:
        v.update_from(vertexs[0][0])
    for i in range(1, vertexs.__len__() - 1):
        node_array = vertexs[i]
        if node_array is None:
            continue
        for node in node_array:
            if node.vertex_from is None:
                continue
            for node_to in vertexs[i + len(node.real_word)]:
                node_to.update_from(node)
    vertex_from = vertexs[-1][0]
    vertex_list = []
    while vertex_from is not None:
        vertex_list.insert(0, vertex_from)
        vertex_from = vertex_from.vertex_from
    return vertex_list

def viterbi_roletag(roletaglist, hmm):
    _length = len(roletaglist)
    taglist = []
    # 得到第一个元素的第一个标签的词性
    _pre_nature = roletaglist[0].nature
    _perfect_nature = _pre_nature
    taglist.append(_pre_nature)
    for i in xrange(1, _length):
        perfect_cost = DOUBLE_MAX
        item = roletaglist[i]
        for i, nature, freq in item.natures:
            _now = hmm.trans_prob[_pre_nature.index][nature.index] - math.log((item.get_nature_frequency(nature)+1e-8) / hmm.get_total_freq(nature))
            if perfect_cost > _now:
                perfect_cost = _now
                _perfect_nature = nature
        _pre_nature = _perfect_nature
        taglist.append(_pre_nature)
    return taglist

def viterbi_template(node_list, hmm, init_cost=DOUBLE_MAX):
    node_count = len(node_list)
    taglist = []
    # 得到第一个元素的第一个标签的词性
    _pre_nature = node_list[0].nature
    _perfect_nature = _pre_nature
    taglist.append(_pre_nature)
    for i, cur_node in enumerate(node_list[1:]):
        perfect_cost = init_cost
        for j, vertex, freq in cur_node.natures:
            _now = hmm.trans_prob[_pre_nature.index][vertex.index] - math.log(
                (cur_node.get_nature_frequency(vertex) + 1e-8) / hmm.get_total_freq(vertex))
            if perfect_cost > _now:
                perfect_cost = _now
                _perfect_nature = vertex
        _pre_nature = _perfect_nature
        taglist.append(_pre_nature)
    return taglist


def viterbi_standard(node_list, hmm, init_cost=DOUBLE_MAX):
    node_count = len(node_list)
    taglist = []
    # 得到第一个元素的第一个标签的词性
    route_cost = []
    _pre_nature = node_list[0].nature
    _perfect_nature = _pre_nature
    taglist.append(_pre_nature)

    # 计算第2个元素
    current_line = node_list[1]
    for i, vertex, freq in current_line.natures:
        _now = hmm.trans_prob[_pre_nature.index][vertex.index] - math.log(
            (current_line.get_nature_frequency(vertex) + 1e-8) / hmm.get_total_freq(vertex))
        route_cost.append(_now)
    pre_line = current_line

    # 计算第三个元素
    for i, current_line in enumerate(node_list[2:]):
        new_route_cost = []
        perfect_pre_nature = None
        perfect_cost = init_cost
        for k, cur_nature, cur_freq in current_line.natures:
            new_route_cost.append(init_cost)
            for j, pre_nature, pre_freq in pre_line.natures:
                assert j < len(route_cost)

                _now = route_cost[j] + hmm.trans_prob[pre_nature.index][cur_nature.index] - math.log(
                    (current_line.get_nature_frequency(cur_nature) + 1e-8) / hmm.get_total_freq(cur_nature))

                if new_route_cost[k] > _now:
                    new_route_cost[k] = _now
                    if perfect_cost > _now:
                        perfect_cost = _now
                        perfect_pre_nature = pre_nature

        pre_line = current_line
        route_cost = new_route_cost
        if Config.debug:
            print new_route_cost
        taglist.append(perfect_pre_nature)
    taglist.append(cur_nature)
    return taglist

