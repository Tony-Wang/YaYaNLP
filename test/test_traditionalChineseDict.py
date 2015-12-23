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
        text = u"記者羅吉訓／新竹報導 雙方合作的主要內容包括，希望能夠促成太陽能設備安裝維修人才培養；" \
               u"結合推廣教育由綠野集團引薦國外學生來臺就讀；與觀光及餐飲系合作觀光休閒產業，" \
               u"提供來臺遊客入住大華科大樂群會館，並導覽參訪張學良故居等臺灣各知名景點。 " \
               u"訂閱聯絡電話：02-23222722-814 瀏覽器建議使用IE 9.0以上版本 最佳觀看解析度1024x768 " \
               u"網站更新日期：2015/12/13 "
        simplified = TraditionalChineseDict().convert_traditional_to_simplified(text)
        print(simplified)
        text = u"媒體詢問對目前選戰看法？朱立倫說最重要是要把沉默的大眾喚出來，" \
               u"為了台灣安定、兩岸和平及經濟發展，拜託大家在最後關頭全力團結及共同支持。 " \
               u"今晚黨內重量級人士到齊，媒體詢問等於是最高規格的選戰會議，" \
               u"是否會向總統當面拜託總統夫人周美青出來？朱立倫馬上向身旁的馬總統說，" \
               u"「對呀，請馬學長拜託周學姐出來輔選」，總統笑著說「我一定轉達」。 " \
               u"朱立倫表示，今晚餐敘不是輔選會報，但不管是馬總統、吳副總統、王金平及行政院長毛治國，" \
               u"大家都是同心協力，求團結勝選 。 他強調，最近到各地陸續見到好多民眾展現熱情，" \
               u"希望最後一個月不斷加溫，直到明年1月16日勝選。1041217 這裡有個好粉絲團，需要你關注！"
        simplified = TraditionalChineseDict().convert_traditional_to_simplified(text)
        print(simplified)
