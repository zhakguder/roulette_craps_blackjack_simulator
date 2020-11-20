#!/usr/bin/env python3


class Bin:
    """Contains a collection of Outcome objects that which reflect the winning bets
that are paid for a particular bin on a Roulette wheel."""

    def __init__(self, *outcomes):
        self.outcomes = outcomes

    def add(self, outcome):
        """Adds an outcome to the bin."""
        self.outcomes = self.outcomes + outcome

    def __str__(self):
        return ", ".join(map(str, self.outcomes))
