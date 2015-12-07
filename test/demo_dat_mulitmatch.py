# -*- coding:utf-8 -*-
import codecs
import time

from yaya.collection.dict import DoubleArrayTrie

__author__ = 'tony'


def main():
    f = codecs.open("./test/data/我的团长我的团.txt", 'r', "utf-8")
    text = f.read()
    search = DoubleArrayTrie.buildcoredictsearcher(text)
    i = 0
    start = time.time()
    while search.next():
        i += 1
        pass
    print "分词时间: %s" % (time.time() - start)
    print "分词个数: %s" % i
    print "词典大小: %s" % search.trie.keySize
    print "文本大小: %s" % len(text)

if __name__ == '__main__':
    main()
