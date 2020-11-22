#!/usr/bin/env python3
from src.bet import Bet


class Player1326State:
    """Super class for all the states in the 1-3-2-6 betting system
        Attrs:
            player (Player1326): The player who is currently in this state.
    """

    def __init__(self, player):
        self.player = player

    def current_bet(self):
        """Constructs a new Bet from the player's outcome information."""
        raise NotImplementedError

    def next_won(self):
        """Constructs the new Player1326State instance to be used when the bet was a winner."""
        raise NotImplementedError

    def next_loss(self):
        """Constructs the new Player1326State instance to be used when the bet was a loser."""
        return Player1326NoWins(self.player)


class Player1326NoWins(Player1326State):
    def current_bet(self):
        """Constructs a bet from the players outcome information. Bet multiplier is 1."""
        amount = self.player.base_bet
        return Bet(self.player.outcome, amount)

    def next_won(self):
        """Constructs a new player Player1326OneWin instance to be used when the bet was a winner."""
        return Player1326OneWin(self.player)


class Player1326OneWin(Player1326State):
    def current_bet(self):
        """Constructs a bet from the players outcome information. Bet multiplier is 3"""
        amount = self.player.base_bet * 3
        return Bet(self.player.outcome, amount)

    def next_won(self):
        """Constructs a new player Player1326TwoWins instance to be used when the bet was a winner."""
        return Player1326TwoWins(self.player)


class Player1326TwoWins(Player1326State):
    def current_bet(self):
        """Constructs a bet from the players outcome information. Bet multiplier is 2."""
        amount = self.player.base_bet * 2
        return Bet(self.player.outcome, amount)

    def next_won(self):
        """Constructs a new player Player1326ThreeWins instance to be used when the bet was a winner."""
        return Player1326ThreeWins(self.player)


class Player1326ThreeWins(Player1326State):
    def current_bet(self):
        """Constructs a bet from the players outcome information. Bet multiplier is 6."""
        amount = self.player.base_bet * 6
        return Bet(self.player.outcome, amount)

    def next_won(self):
        """Constructs a new player Player1326NoWins instance to be used when the bet was a winner."""
        return Player1326NoWins(self.player)
