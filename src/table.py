#!/usr/bin/env python3
from src.bet import InvalidBet


class Table:
    """Table contains all Bets created by a player. It has a betting limit. The sum
    of all of a player's bets should be less than or equal to this limit. We assume
    a single player in the simulation.
    """

    def __init__(self, limit):
        self.limit = limit
        self.bets = []

    def is_valid(self, bet):
        """If the sum of all bets is less than or equal to the table limit,the bet is valid."""
        return (
            sum([x.lose_amount() for x in self.bets]) + bet.lose_amount() <= self.limit
        )

    def place_bet(self, bet):
        """Add this bet to the list of working bets. If the sum of all bets is greater
       than the table limit, then InvalidBet exception is thrown."""
        if not self.is_valid(bet):
            raise InvalidBet("Table bet limit exceeded.")
        self.bets.append(bet)

    def __iter__(self):
        """Returns an iterator over the list of bets."""
        return iter(self.bets)

    def __str__(self):
        """Prints all placed bets in the table."""
        "\n".join([str(x) for x in self.bets])
