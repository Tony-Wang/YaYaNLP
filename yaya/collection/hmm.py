# coding=utf-8
from __future__ import unicode_literals
import math

from yaya.common.ns import NS
from yaya import config
from yaya.common.nr import NR
from yaya.common.nt import NT
from yaya.utility.singleton import singleton

__author__ = 'tony'


class HMMMatrix:
    def __init__(self):
        self.matrix = []
        self.total = None
        self.total_freq = 0
        self.start_prob = None
        self.trans_prob = None

    def get_total_freq(self, nature):
        return self.total[nature.index]

    @staticmethod
    def load(filename, cls):
        with open(filename, 'r') as f:
            flist = f.read().splitlines()
        labels = flist[0].split(',')[1:]
        ord_array = [[0]] * len(labels)
        ord_max = 0
        for i in range(len(ord_array)):
            ord_array[i] = cls[labels[i]].index
            ord_max = max(ord_max, ord_array[i])
        # 找到最大的枚举值
        ord_max += 1
        hmm = HMMMatrix()
        hmm.matrix = [[0 for col in range(ord_max)] for row in range(ord_max)]
        for row in flist[1:]:
            params = row.split(',')
            cur_ord = cls[params[0]].index
            for i in range(ord_array.__len__()):
                hmm.matrix[cur_ord][ord_array[i]] = int(params[1 + i])

        hmm.total = [[0]] * ord_max
        for j in range(ord_max):
            hmm.total[j] = 0
            for i in range(ord_max):
                hmm.total[j] += hmm.matrix[i][j]

        for j in range(ord_max):
            hmm.total[j] += hmm.matrix[j][j]

        for j in range(ord_max):
            hmm.total_freq += hmm.total[j]

        # 计算HMM四元组
        states = ord_array
        hmm.start_prob = [[0]] * ord_max
        for s in ord_array:
            freq = hmm.total[s] + 1e-8
            hmm.start_prob[s] = -math.log(freq / hmm.total_freq)

        hmm.trans_prob = [[0 for col in range(ord_max)] for row in range(ord_max)]
        for f in ord_array:
            for t in ord_array:
                freq = hmm.matrix[f][t] + 1e-8
                hmm.trans_prob[f][t] = -math.log(freq / hmm.total_freq)
        return hmm


@singleton
class PersonTranMatrix:
    def __init__(self):
        self.hmm = HMMMatrix.load(config.PERSON_TR_PATH, NR)


@singleton
class OrgTranMatrix:
    def __init__(self):
        self.hmm = HMMMatrix.load(config.ORG_TR_PATH, NT)

@singleton
class PlaceTranMatrix:
    def __init__(self):
        self.hmm = HMMMatrix.load(config.PLACE_TR_PATH, NS)
