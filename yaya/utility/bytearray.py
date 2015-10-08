from io import FileIO

__author__ = 'tony'
import struct


class ByteArray:
    @staticmethod
    def load_from_file(filename):
        f = FileIO(filename, 'rb')
        data = f.readall()
        return ByteArray(data)

    def __init__(self, data):
        self.data = data
        self.offset = 0

    def has_more(self):
        return self.offset < len(self.data)

    def next_ushort(self):
        data = struct.unpack_from('!h', self.data, self.offset)
        self.offset += 2
        return data[0]

    def next_uchar(self):
        data = struct.unpack_from('!B', self.data, self.offset)
        self.offset += 1
        return data[0]
