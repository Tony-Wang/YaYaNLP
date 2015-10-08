# coding=utf-8
import time
from yaya import config
from yaya.const import logger
from yaya.utility.bytearray import ByteArray

__author__ = 'tony'

CT_SINGLE = 5  # 单字节
CT_DELIMITER = CT_SINGLE + 1  # 分隔符"!,.?()[]{}+=
CT_CHINESE = CT_SINGLE + 2  # 中文字符
CT_LETTER = CT_SINGLE + 3  # 字母
CT_NUM = CT_SINGLE + 4  # 数字
CT_INDEX = CT_SINGLE + 5  # 序号
CT_OTHER = CT_SINGLE + 12  # 其他

char_type = [[]] * 65536


def __init__():
    logger.info("字符类型对应表开始加载 %s", config.CHAR_TYPE_PATH)
    start = time.time()
    byte_array = ByteArray.load_from_file(config.CHAR_TYPE_PATH)
    if byte_array is None:
        import sys
        logger.error("字符类型对应表加载失败：" + config.CHAR_TYPE_PATH)
        sys.exit(-1)
    else:
        while byte_array.has_more():
            b = byte_array.next_ushort()
            e = byte_array.next_ushort()
            t = byte_array.next_uchar()
            for i in range(b, e + 1):
                char_type[i] = t
        logger.info("字符类型对应表加载成功，耗时 %s s", (time.time() - start))


def get(c):
    if type(c) is not int:
        return char_type[ord(c)]
    else:
        return char_type[c]


__init__()
