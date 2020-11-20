#!/usr/bin/env python3

import unittest
from src.outcome import Outcome
from src.bet import Bet


class TestBet(unittest.TestCase):
    def setUp(self):
        self.outcome1 = Outcome("test1", 2)
        self.outcome2 = Outcome("test2", 3)

    def test_win_amount(self):
        bet1 = Bet(self.outcome1, 10)
        bet2 = Bet(self.outcome2, 20)
        self.assertEqual(bet1.win_amount(), 20)
        self.assertEqual(bet2.lose_amount(), 20)
