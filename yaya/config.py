# coding=utf-8
__author__ = 'tony'
import os

DICT_BIN_EXT = '.ya'

DATA_ROOT = "/home/tony/MyProject/YaYaNLP/data"

CUSTOM_DICT_NAME = [os.path.join(DATA_ROOT + "/dictionary/custom/", f) for f in [
    u"CustomDictionary.txt",
    u"上海地名.txt",
    u"人名词典.txt",
    u"全国地名大全.txt",
    u"机构名词典.txt",
    u"现代汉语补充词库.txt"]]

CORE_DICT_NAME = os.path.join(DATA_ROOT, "dictionary/CoreNatureDictionary.txt")
CORE_BIGRAM_NAME = os.path.join(DATA_ROOT, "dictionary/CoreNatureDictionary.ngram.txt")
CHAR_TYPE_PATH = os.path.join(DATA_ROOT, "dictionary/other/CharType.dat.yes")
PERSON_TR_PATH = os.path.join(DATA_ROOT, "dictionary/person/nr.tr.txt")
PERSON_DICT_NAME = os.path.join(DATA_ROOT, "dictionary/person/nr.txt")
