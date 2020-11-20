#!/usr/bin/env python3
from src.outcome import Outcome
from src.bet import Bet
from math import pow

black = Outcome("Black", 1)


class Player:
    """
        Super class of player strategies
        Attrs:
            table (Table): Table player is on
            stake (int): Player's current stake. Initialized to starting budget.
            rounds_to_go (int): Number of rounds to play.
    """

    def __init__(self, a_table):
        self.table = a_table
        self.stake = None
        self.rounds_to_go = None

    def playing(self):
        """Returns True while the player is active"""
        return True

    def place_bets(self):
        self.rounds_to_go -= 1

    def win(self, bet):
        """Updates the user stake with the amount won from bet."""
        self.stake += bet.win_amount()

    def lose(self, bet):
        """Notification from the Game that the bet was a loser."""
        pass

    def set_stake(self, init_stake):
        """Sets the initial stake"""
        self.stake = init_stake

    def set_rounds(self, init_rounds):
        """Sets the inital round"""
        self.rounds_to_go = init_rounds


class MartingalePlayer(Player):
    """Player that plays with Martingale strategy
        Attrs:
            loss_count (int): Number of losses of the player
            bet_multiple (int): Multiplier for the bet. It is 2^(loss_count)
    """

    def __init__(self, a_table):
        super().__init__(a_table)
        self.loss_count = 0
        self.bet_multiple = 1

    def place_bets(self):
        """Updates the table with a bet on black. The amount bet is bet_multiple"""
        super().place_bets()
        self.table.place_bet(Bet(black, self.bet_multiple))
        self.stake -= self.bet_multiple

    def win(self, bet):
        """
         loss_count will be set to 0 and bet_multiple will be reset to 1.
         """
        super().win(bet)
        self.loss_count = 0
        self.bet_multiple = 1

    def lose(self, bet):
        """Increments loss count by 1 and doubles bet_multiple"""
        self.loss_count += 1
        self.bet_multiple *= 2

    def playing(self):
        return self.stake >= self.bet_multiple and self.rounds_to_go > 0


class Passenger57(Player):
    def __init__(self, a_table):
        super().__init__(a_table)

    def place_bets(self):
        super().place_bets()
        bet_amount = 10
        if self.stake >= bet_amount:
            self.table.place_bet(Bet(black, bet_amount))
            self.stake -= bet_amount

    def win(self, bet):
        super().win(bet)

    def lose(self, bet):
        pass

    def playing(self):
        return True
