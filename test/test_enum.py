from unittest import TestCase

from yaya.common.enum import Enum, EnumValue
from yaya.common.nr import NR
from yaya.common.nature import NATURE

__author__ = 'tony'


class TestEnum(TestCase):
    def test_nr(self):
        self.assertEqual(NR.A.index, 14)

    def test_nature(self):
        self.assertEqual(NATURE.n.index, 13)

    def test_nature_key_to_index(self):
        self.assertEqual(type(NATURE.n), EnumValue)

    def test_nature_key_to_str(self):
        self.assertEqual(str(NATURE.n), 'n')

    def test_enum(self):
        E1 = Enum('a', 'b')
        self.assertTrue(str(E1.b) == 'b')
        self.assertEqual(E1['b'].index, 1)

    def test_demo(self):
        # char => int
        E1 = Enum('a', 'b')
        self.assertTrue(str(E1.b) == 'b')
        self.assertEqual(E1['b'].index, 1)
        self.assertTrue(str(E1[1]) == 'b' )