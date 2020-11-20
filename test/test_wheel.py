#!/usr/bin/env python3

import unittest
from src.outcome import Outcome
from src.bin import Bin
from src.wheel import Wheel

from test.non_random import NonRandom


class TestWheel(unittest.TestCase):
    def setUp(self):
        self.outcome1 = Outcome("abc", 2)
        self.outcome2 = Outcome("def", 3)
        self.outcome3 = Outcome("ghi", 4)
        self.outcome4 = Outcome("jkl", 5)

        self.bin1 = Bin(self.outcome1, self.outcome2, self.outcome3)
        self.bin2 = Bin(self.outcome2, self.outcome3, self.outcome4)

        self.wheel = Wheel(NonRandom())
        self.wheel.set_bin(0, self.bin1)
        self.wheel.set_bin(1, self.bin2)

    def test_can_add_bins(self):

        self.assertEqual(self.wheel.get_bin(0), self.bin1)
        self.assertEqual(self.wheel.get_bin(1), self.bin2)

    def test_rng(self):
        for i in range(12):
            print(self.wheel.next())
            print(self.wheel.next())
