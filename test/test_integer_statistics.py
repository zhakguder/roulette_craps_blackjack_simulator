#!/usr/bin/env python3

from src.integer_statistics import mean, stdev

import unittest


class TestIntegerStatistics(unittest.TestCase):
    def setUp(self):
        self.list = [9, 8, 5, 9, 9, 4, 5, 8, 10, 7, 8, 8]

    def test_mean(self):
        self.assertAlmostEqual(mean(self.list), 7.5)

    def test_stdev(self):
        self.assertAlmostEqual(stdev(self.list), 1.88293774)
