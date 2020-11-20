#!/usr/bin/env python3

import unittest
from src.bin import Bin
from src.outcome import Outcome


class TestBin(unittest.TestCase):
    def setUp(self):
        self.outcome1 = Outcome("abc", 1)
        self.outcome2 = Outcome("def", 2)
        self.outcome3 = Outcome("ghi", 3)
        self.outcome4 = Outcome("jkl", 4)

        self.bin1 = Bin(self.outcome1, self.outcome2, self.outcome3)
        self.bin2 = Bin(self.outcome2, self.outcome3, self.outcome4)

    def test_bin(self):
        intersect = set(self.bin1.outcomes).intersection(set(self.bin2.outcomes))
        self.assertEqual(len(intersect), 2)
