#!/usr/bin/env python3


class Bet:
    """A Bet is an amount that a player has wagered on an outcome

        Args:
            outcome (str): outcome the bet is made on
            amount (str): how much money is bet on the outcome

    """

    def __init__(self, outcome, amount):
        self.outcome = outcome
        self.amount = amount

    def win_amount(self):
        """Computes the amount won including the amount bet"""
        return self.outcome.win_amount(self.amount) + self.amount

    def lose_amount(self):
        """Returns the amount lost. This is the amount bet"""
        return self.amount

    def __str__(self):
        return str(self.outcome)


class InvalidBet(Exception):
    pass
