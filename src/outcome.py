#!/usr/bin/env python3


class Outcome:
    """Contains a single outcome on which a bet can be placed.

        Attributes:
             name (str): name of the outcome
             odds (int): payout odds for the outcome. Only the nominator is kept, denominator is assumed to be 1.

    """

    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def win_amount(self, amount):
        """Multiplies the outcome's odds with amount and returns the result"""
        return self.odds * amount

    def __str__(self):
        return f"{self.name}\t({self.odds}:1)"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        """Defines equality of two Outcome objects"""
        return self.name == other.name

    def __ne__(self, other):
        return not self == other
