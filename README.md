# YaYaNLP: Chinese Language Processing
YaYaNLP是一个纯python编写的中文自然语言处理包，取名于“牙牙学语”。
YaYaNLP提供以下功能：
- 中文分词
- 词性标注
- 命名实体识别
 * 人名识别
 * 地名识别
 * 组织机构识别
- 简繁转换
## 项目
项目主页：[https://github.com/Tony-Wang/YaYaNLP](https://github.com/Tony-Wang/YaYaNLP)
我的主页：[www.huangyong.me](http://wwww.huangyong.me)
## 安装
### 直接下载源码包，解压后运行
``` bash
python setup.py install
```

### 下载字典与模型文件
YaYaNLP使用了与HanLP兼容的字典数据，而编译后的字典数据保存的扩展名为.ya
可以直接从hanLP项目下载，[data-for-1.2.4.zip](http://pan.baidu.com/s/1gd1vo8j)

### 配置数据文件路径
在**yaya/const.py**修改自己的数据文件路径
``` python
DATA_ROOT = "/your/data/path"
```

## 使用

``` python
# -*- coding=utf-8 -*-
from yaya.seg import segment


def print_terms(terms):
    for i, v in enumerate(terms):
        print v[0], v[1], v[2]


def main():
    # 识别人名
    text = u"签约仪式前，秦光荣、李纪恒、仇和等一同会见了参加签约的企业家。"
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
```

## 感谢
本项目参考了[hanck/HanLP](https://github.com/hankcs/HanLP/)项目实现原理并使用了该项目的字典和模型文件。
