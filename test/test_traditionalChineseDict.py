# coding=utf-8
from unittest import TestCase

from yaya import config
from yaya.dictionary.chinese_traditional_dict import TraditionalChineseDict, SimplifiedChineseDict

__author__ = 'tony'


class TestTraditionalChineseDict(TestCase):
    def test_convert_simplified_to_traditional(self):
        simplified = TraditionalChineseDict().convert_traditional_to_simplified(u"用筆記簿型電腦寫程式HelloWorld")
        self.assertEqual(simplified, u"用笔记本电脑写程序HelloWorld")

    def test_convert_traditional_to_simplified(self):
        config.Config.debug = True
        traditional = SimplifiedChineseDict().convert_simplified_to_traditional(u"用笔记本电脑写程序HelloWorld")
        self.assertEqual(traditional, u"用筆記簿型電腦寫程式HelloWorld")

    def test_traditional_chinese_dict_search_all_words(self):
        searcher = TraditionalChineseDict().trie.search(u"用筆記簿型電腦寫程式HelloWorld")
        for i, k, v in searcher.search_all_words():
            print i, k, v

    def test_demo1(self):
        text = u"記者羅吉訓／新竹報導 雙方合作的主要內容包括，希望能夠促成太陽能設備安裝維修人才培養；結合推廣教育由綠野集團引薦國外學生來臺就讀；與觀光及餐飲系合作觀光休閒產業，提供來臺遊客入住大華科大樂群會館，並導覽參訪張學良故居等臺灣各知名景點。 訂閱聯絡電話：02-23222722-814 瀏覽器建議使用IE 9.0以上版本 最佳觀看解析度1024x768 網站更新日期：2015/12/13 "
        simplified = TraditionalChineseDict().convert_traditional_to_simplified(text)
        print(simplified)
