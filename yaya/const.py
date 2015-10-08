# coding=utf-8
import logging
from collections import namedtuple

__author__ = 'tony'

logger = logging.getLogger("YaYaNLP")

# 算术常量
DOUBLE_MAX = 1.7976931348623157e+308

# 预定义常量
TAG_PLACE = u"未##地"
TAG_BIGIN = u"始##始"
TAG_OTHER = u"未##它"
TAG_GROUP = u"未##团"
TAG_NUMBER = u"未##数"
TAG_QUANTIFIER = u"未##量"
TAG_PROPER = u"未##专"
TAG_TIME = u"未##时"
TAG_CLUSTER = u"未##串"
TAG_END = u"末##末"
TAG_PEOPLE = u"未##人"

# 总词频
MAX_FREQUENCY = 25146057
SMOOTHING_FACTOR = 1.0 / MAX_FREQUENCY + 0.00001
SMOOTHING_PARAM = 0.1
