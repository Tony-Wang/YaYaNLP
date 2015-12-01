# coding=utf-8
from yaya.seg import segment

__author__ = 'tony'


def print_terms(terms):
    for i, v in enumerate(terms):
        print v[0], v[1], v[2]


def main():
    # 识别人名
    text = u"签约仪式前，秦光荣、李纪恒、仇和、王春桂等一同会见了参加签约的企业家。"
    terms = segment.seg(text)
    print_terms(terms)

    # 识别地名
    text = u"蓝翔给宁夏固原市彭阳县红河镇黑牛沟村捐赠了挖掘机"
    terms = segment.seg(text)
    print_terms(terms)

    # 简繁转换
    text = u"以后等你当上皇后，就能买草莓庆祝了"
    print segment.simplified_to_traditional(text)

    # 繁简转换
    text = u"用筆記簿型電腦寫程式HelloWorld"
    print segment.traditional_to_simplified(text)


if __name__ == '__main__':
    main()
