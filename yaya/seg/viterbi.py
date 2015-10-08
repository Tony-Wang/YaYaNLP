# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from yaya.const import DOUBLE_MAX

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


def viterbi(word_net):
    for v in word_net.vertexs[1]:
        v.update_from(word_net.vertexs[0][0])
    for i in range(1, word_net.vertexs.__len__() - 1):
        node_array = word_net.vertexs[i]
        if node_array is None:
            continue
        for node in node_array:
            if node.vertex_from is None:
                continue
            for node_to in word_net.vertexs[i + node.real_word.__len__()]:
                node_to.update_from(node)
    vertex_from = word_net.vertexs[-1][0]
    vertex_list = []
    while vertex_from is not None:
        vertex_list.insert(0, vertex_from)
        vertex_from = vertex_from.vertex_from
    return vertex_list
