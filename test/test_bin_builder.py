#!/usr/bin/env python3

import unittest
from src.bin_builder import BinBuilder
from src.wheel import Wheel


class TestBinBuilder(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel()
        self.bin_builder = BinBuilder()

    def test_bin_builder(self):
        self.bin_builder.build_bins(self.wheel)
