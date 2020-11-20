#!/usr/bin/env python3

import unittest
from src.outcome import Outcome


class TestOutcome(unittest.TestCase):
    def setUp(self):
        self.outcome1 = Outcome("abc", 1)
        self.outcome2 = Outcome("abc", 2)
        self.outcome3 = Outcome("bcd", 1)

    def test_equality(self):
        self.assertEqual(
            self.outcome1,
            self.outcome2,
            "Outcomes with same names should be considered equal.",
        )

    def test_inequality(self):
        self.assertNotEqual(
            self.outcome1,
            self.outcome3,
            "Outcomes with different names should be considered unequal.",
        )

    def test_hash_equality(self):
        self.assertEqual(
            hash(self.outcome1),
            hash(self.outcome2),
            "Outcomes with the same name should have equal hash values.",
        )

    def test_win_amount(self):
        self.assertEqual(self.outcome1.win_amount(10), 10, "Wrong outcome win amount.")
        self.assertEqual(self.outcome2.win_amount(10), 20, "Wrong outcome win amount.")
