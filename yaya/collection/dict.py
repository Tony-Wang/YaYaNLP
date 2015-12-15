# -*- coding:utf-8 -*-
import cPickle as Pickle
from collections import OrderedDict

from yaya.const import *
from yaya import config
from yaya.utility.singleton import singleton
from yaya.common.nature import NATURE

ATTRIBUTE_MAIN_NATURE_INDEX = 0


class Node(object):
    def __init__(self, code=0, depth=0, left=0, right=0):
        self.code = code
        self.depth = depth
        self.left = left
        self.right = right


class Attribute(object):
    def __init__(self, attr, cls=NATURE):
        self.cls = cls
        self.total = 0
        if not isinstance(attr, tuple):
            self.data = ()
            if attr is not None:
                attr = attr if isinstance(attr, list) else attr.split(' ')
                nature = []
                for i in range(0, attr.__len__(), 2):
                    nature.append(cls[attr[i]])
                    nature.append(int(attr[i + 1]))
                    self.total += int(attr[i + 1])
                self.data = tuple(nature)
        else:
            self.data = attr
            for i in range(len(self.data)):
                if i % 2 == 1:
                    self.total += self.data[i]

    def to_tuple(self):
        return self.data

    def __str__(self):
        return ' '.join([str(x) for x in self.data])

    def __repr__(self):
        return u"Attribute(%s)" % self.__str__()

    def __len__(self):
        return len(self.data) / 2

    def get_nature_frequency(self, nature):
        try:
            return self.data[self.data.index(nature) + 1]
        except:
            return 0

    @property
    def natures(self):
        for i in range(0, len(self.data), 2):
            yield self.data[i], self.data[i + 1]
            # return self.data

    @property
    def nature(self):
        if self.data.__len__() != 0:
            return self.data[ATTRIBUTE_MAIN_NATURE_INDEX]
        else:
            return None

    @property
    def total_frequency(self):
        return self.total


class DoubleArrayTrie:
    def __init__(self):
        self.alloc_size = 0
        self.check = []
        self.base = []

        self.used = []
        self.size = 0
        self.key = []
        self.key_size = 0
        self.length = None
        self.value = []
        self.v = None
        self.progress = 0
        self.next_check_pos = 0
        self.error_ = 0

    def word_size(self):
        if self.v is None:
            return 0
        else:
            return self.v.__len__()

    def resize(self, newsize):
        offsize = newsize - self.alloc_size
        self.base.extend([0] * offsize)
        self.check.extend([0] * offsize)
        self.used.extend([0] * offsize)
        self.alloc_size = newsize


    def fetch(self, parent, siblings):
        if self.error_ < 0:
            return 0
        prev = 0
        for i in xrange(parent.left, parent.right):
            if parent.depth > (self.length[i] if self.length is not None else self.key[i].__len__()):
                continue
            tmp = self.key[i]
            cur = 0
            if (self.length[i] if self.length is not None else tmp.__len__()) != parent.depth:
                cur = ord(tmp[parent.depth]) + 1

            # 检测是不是字典序
            if prev > cur:
                return 0

            if cur != prev or siblings.__len__() is 0:
                tmp_node = Node(depth=parent.depth + 1, code=cur, left=i, right=0)
                if siblings.__len__() != 0:
                    siblings[-1].right = i
                siblings.append(tmp_node)
            prev = cur

        if siblings.__len__() != 0:
            siblings[-1].right = parent.right

        return siblings.__len__()

    def insert(self, siblings):
        if self.error_ < 0:
            return 0

        begin = 0
        pos = (siblings[0].code + 1 if (siblings[0].code + 1 > self.next_check_pos) else self.next_check_pos) - 1
        nonzero_num = 0
        first = 0

        if self.alloc_size <= pos:
            self.resize(pos + 1)

        while 1:
            pos += 1

            if self.alloc_size <= pos:
                self.resize(pos + 1)

            if self.check[pos] != 0:
                nonzero_num += 1
                continue
            elif first is 0:
                self.next_check_pos = pos
                first = 1

            begin = pos - siblings[0].code

            if self.alloc_size <= (begin + siblings[-1].code):
                if 1.05 > 1.0 * self.key_size / (self.progress + 1):
                    l = 1.05
                else:
                    l = 1.0 * self.key_size / (self.progress + 1)
                self.resize(int(self.alloc_size * l))

            if self.used[begin]:
                continue

            find = True
            for i in xrange(siblings.__len__()):
                if self.check[begin + siblings[i].code] != 0:
                    find = False
                    break
            if not find:
                continue
            break

        if 1.0 * nonzero_num / (pos - self.next_check_pos + 1) >= 0.95:
            self.next_check_pos = pos

        self.used[begin] = True
        self.size = self.size if (self.size > begin + siblings[-1].code + 1) else \
            begin + siblings[-1].code + 1

        for i in xrange(siblings.__len__()):
            self.check[begin + siblings[i].code] = begin

        for i in xrange(siblings.__len__()):
            new_siblings = []

            if self.fetch(siblings[i], new_siblings) is 0:
                self.base[begin + siblings[i].code] = -self.value[siblings[i].left] - 1 if (
                    self.value is not None) else (-siblings[i].left - 1)

                if self.value is not None and -self.value[siblings[i].left] - 1 >= 0:
                    self.error_ = -2
                    return 0

                self.progress += 1
            else:
                h = self.insert(new_siblings)
                self.base[begin + siblings[i].code] = h

        return begin

    def build(self, key=None, length=None, keysize=None, v=None):
        if keysize > key.__len__() or key is None:
            return 0

        self.key = key
        self.length = length
        self.key_size = keysize if keysize is not None else key.__len__()
        self.value = None
        self.v = v if v is not None else key
        self.progress = 0

        self.resize(65536 * 32)

        self.base[0] = 1
        self.next_check_pos = 0

        root_node = Node(left=0, right=self.key_size, depth=0, code=0)

        siblings = []
        self.fetch(root_node, siblings)
        self.insert(siblings)

        self.key = None

        return self.error_

    def exact_match_search(self, key, pos=0, keylen=0, nodepos=0):
        if key is None:
            return -1
        if keylen <= 0:
            keylen = key.__len__()
        if nodepos <= 0:
            nodepos = 0

        result = -1
        b = self.base[nodepos]

        for i in xrange(pos, keylen):
            p = b + ord(key[i]) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return result

        p = b
        n = self.base[p]
        if b == self.check[p] and n < 0:
            result = -n - 1
        return result

    def get(self, word):
        index = self.exact_match_search(word)
        if index >= 0:
            return index, self.v[index]
        else:
            return index, None

    # def get_attribute(self, key):
    #     index, value = self.get(key)
    #     if value is not None:
    #         value = Attribute(value[1:])
    #     return value

    def transition(self, path, state_from):
        b = state_from
        for i in range(len(path)):
            p = b + ord(path[i]) + 1
            if b == self.check[p]:
                b = self.base[p]
            else:
                return -1
        p = b
        return p

    def output(self, state):
        if state < 0:
            return None
        n = self.base[state]
        if state == self.check[state] and n < 0:
            return self.v[-n - 1]
        return None

    def dump(self):
        for i in range(self.size):
            print("i: %s [%s,%s]" % (i, self.base[i], self.check[i]))

    def compress(self):
        last = self.alloc_size - 1
        while self.used[last] == 0:
            last -= 1
        self.base = self.base[:last + 1]
        self.check = self.check[:last + 1]
        self.alloc_size = len(self.base)

    @staticmethod
    def save_to_ya(trie, filename):
        # trie.compress()
        import cPickle as Pickle
        with open(filename, 'w') as f:
            Pickle.dump(trie, f, protocol=Pickle.HIGHEST_PROTOCOL)
            f.close()

    @staticmethod
    def load_bin(filename):
        with open(filename, 'r') as f:
            trie = Pickle.load(f)
            return trie

    @staticmethod
    def load_dict_file(filenames, key_func=None, value_func=None, enum_cls=NATURE):
        import codecs
        k, v, dict_list = [], [], []
        if not isinstance(filenames, list):
            filenames = [filenames]

        for filename in filenames:
            with codecs.open(filename, 'r', 'utf-8') as f:
                dict_list += f.read().splitlines()

        return DoubleArrayTrie.load_from_list(dict_list, key_func, value_func, enum_cls)

    @staticmethod
    def load_from_list(dict_list, key_func=None, value_func=None, enum_cls=NATURE):
        key_func = key_func or (lambda i: i.split()[0])
        value_func = value_func or (lambda i: Attribute(i.split(chr(32))[1:], cls=enum_cls))
        # sort
        dict_map = {}
        for i in dict_list:
            # value = value_func(i)
            # if isinstance(value, str):
            #     value = value.split(chr(32))[1:]
            i = i.replace('\t', chr(32))
            dict_map[key_func(i)] = value_func(i)  # 此处需要解开成列表，viterbi会直接用到
        dict_map = OrderedDict(sorted(dict_map.items()))
        trie = DoubleArrayTrie()
        trie.build(key=dict_map.keys(), v=dict_map.values())
        return trie

    def search(self, key, offset=0):
        return Searcher(self, key, offset)

    @staticmethod
    def load(filenames, key_func=None, value_func=None,
             dict_bin_ext=config.DICT_BIN_EXT, enum_cls=NATURE):
        import os
        # 考虑用户自定义宝典输入为列表的情况
        filename = filenames[0] if type(filenames) is list else filenames
        if config.Config.use_dict_cache and os.path.exists(filename + dict_bin_ext):
            return DoubleArrayTrie.load_bin(filename + dict_bin_ext)
        trie = DoubleArrayTrie.load_dict_file(filenames, key_func, value_func, enum_cls)
        DoubleArrayTrie.save_to_ya(trie, filename + dict_bin_ext)
        return trie

    @staticmethod
    def buildcoredictsearcher(key, offset=0):
        return DoubleArrayTrie().load(config.CORE_DICT_NAME).search(key, offset)


class Searcher:
    def __init__(self, trie, chararray, offset=0):
        # key的起点
        self.begin = 0
        # key的长度
        self.length = 0
        # key的字典序坐标
        self.index = 0
        self.key = None

        # key对应的value
        self.value = None

        # 传入的字符数组
        self.code_array = [ord(c) for c in chararray]

        self.char_array = chararray

        # 上一个node位置
        self.trie = trie
        self.last = trie.base[0]

        # charArray的长度，效率起见，开个变量
        self.array_length = chararray.__len__()

        # 上一个字符的下标
        self.i = offset - 1
        # // A trick，如果文本长度为0的话，调用next()时，会带来越界的问题。
        self.begin = -1 if (self.array_length is 0) else offset

    # 是否命中，当返回false表示搜索结束，否则使用公开的成员读取命中的详细信息
    def next(self):
        b = self.last
        while 1:
            self.i += 1
            if self.i == self.array_length:  # 指针到头了，将起点往前挪一个，重新开始，状态归零
                self.begin += 1
                if self.begin == self.array_length:
                    break
                self.i = self.begin
                b = self.trie.base[0]

            p = b + self.code_array[self.i] + 1  # 状态转移 p = base[char[i-1]] + char[i] + 1
            if b == self.trie.check[p]:  # base[char[i-1]] == check[base[char[i-1]] + char[i] + 1]
                b = self.trie.base[p]  # 转移成功
            else:
                self.i = self.begin  # 转移失败，也将起点往前挪一个，重新开始，状态归零
                self.begin += 1
                if self.begin is self.array_length:
                    break
                b = self.trie.base[0]
                continue
            p = b
            n = self.trie.base[p]
            if b == self.trie.check[p] and n < 0:  # base[p] == check[p] && base[p] < 0 查到一个词
                self.length = self.i - self.begin + 1
                self.index = -n - 1
                self.key = self.char_array[self.begin:self.begin + self.length]
                self.value = self.trie.v[self.index]
                self.last = b
                return True
        return False

    def search_all_words(self):
        b = self.last
        while 1:
            self.i += 1
            if self.i == self.array_length:  # 指针到头了，将起点往前挪一个，重新开始，状态归零
                self.begin += 1
                if self.begin == self.array_length:
                    break
                self.i = self.begin
                b = self.trie.base[0]

            p = b + self.code_array[self.i] + 1  # 状态转移 p = base[char[i-1]] + char[i] + 1
            if b == self.trie.check[p]:  # base[char[i-1]] == check[base[char[i-1]] + char[i] + 1]
                b = self.trie.base[p]  # 转移成功
            else:
                self.i = self.begin  # 转移失败，也将起点往前挪一个，重新开始，状态归零
                self.begin += 1
                if self.begin is self.array_length:
                    break
                b = self.trie.base[0]
                continue
            p = b
            n = self.trie.base[p]
            if b == self.trie.check[p] and n < 0:  # base[p] == check[p] && base[p] < 0 查到一个词
                self.length = self.i - self.begin + 1
                self.index = -n - 1
                self.key = self.char_array[self.begin:self.begin + self.length]
                self.value = self.trie.v[self.index]
                self.last = b
                yield self.begin, self.key, self.value
        return




        # def seek(self,index):
        #     self.i = index -1
        #     self.begin = index
        #     self.last = self.trie.base[0]


# class MaxSearcher:
#     def __init__(self, trie, chararray, offset=0):
#         self.searcher = trie.search(chararray)
#         self.textbegin = 0
#         self.textend = 0
#
#     def next(self):
#         prekey = None
#         preindex = None
#         prebegin = None
#         preend = None
#
#         while self.searcher.next():
#             if prekey == None or prekey == self.searcher.key[:len(prekey)] :
#                 prekey = self.searcher.key
#                 preindex = self.searcher.index
#                 prebegin = self.searcher.begin
#                 preend = self.searcher.begin+self.searcher.length
#                 continue
#             else:
#                 self.key = prekey
#                 self.value = self.searcher.trie.v[preindex]
#                 self.textbegin = prebegin
#                 self.textend = preend
#                 # 需要将起点移到找到的词的后一个
#                 self.searcher.seek(self.textend)
#                 return True
#         return False




@singleton
class CoreDict:
    def __init__(self):
        self.trie = DoubleArrayTrie.load(config.CORE_DICT_NAME)


def __split_id_attribute(item):
    index = item[0]
    value = item[1]
    if isinstance(value, str):
        value = value.split()
    if isinstance(value, list):
        value = value[1:]
    return index, value


PERSON_WORD_ID, PERSON_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_PEOPLE))
PLACE_WORD_ID, PLACE_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_PLACE))
ORG_WORD_ID, ORG_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_GROUP))
PROPER_WORD_ID, PROPER_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_PROPER))
TIME_WORD_ID, TIME_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_TIME))
NUMBER_WORD_ID, NUMBER_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_NUMBER))
CLUSTER_WORD_ID, CLUSTER_ATTRIBUTE = __split_id_attribute(CoreDict().trie.get(TAG_CLUSTER))

@singleton
class CustomDict:
    def __init__(self):
        self.trie = DoubleArrayTrie.load(config.CUSTOM_DICT_NAME)
