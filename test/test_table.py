#!/usr/bin/env python3

import unittest
from src.bet import Bet
from src.table import Table
from src.outcome import Outcome


class TestTable(unittest.TestCase):
    def setUp(self):
        self.bet1 = Bet(Outcome("test1", 2), 100)
        self.bet2 = Bet(Outcome("test2", 3), 200)
        self.table1 = Table(250)
        self.table2 = Table(300)

    def test_table(self):
        # the first bet is under the table limit
        # so place it in both tables
        self.table1.place_bet(self.bet1)
        self.table2.place_bet(self.bet1)
        # first table limit should be exceeded by the second bet
        self.assertFalse(self.table1.is_valid(self.bet2))
        # second table limit shouldn't be exceeded by the second bet
        self.assertTrue(self.table2.is_valid(self.bet2))
