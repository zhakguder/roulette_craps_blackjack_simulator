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
        # self.rounds_to_go -= 1
        pass

    def win(self, bet):
        """Updates the user stake with the amount won from bet."""
        self.stake += bet.win_amount()

    def lose(self, bet):
        """Notification from the Game that the bet was a loser."""
        pass

    def set_stake(self, init_stake):
        """Sets the initial stake"""
        self.stake = init_stake

    def set_rounds(self, rounds):
        """Sets the number of rounds"""
        self.rounds_to_go = rounds

    def winners(self, outcomes):
        pass

    def can_place_bet(self, amount):
        return self.stake >= amount


class Passenger57(Player):
    def __init__(self, a_table):
        super().__init__(a_table)

    def place_bets(self):
        bet_amount = 10
        if not self.can_place_bet(bet_amount):
            return

        self.table.place_bet(Bet(black, bet_amount))
        self.stake -= bet_amount

    def win(self, bet):
        super().win(bet)

    def lose(self, bet):
        pass

    def playing(self):
        return True


class MartingalePlayer(Player):
    """Player that plays with Martingale strategy
        Attrs:
            loss_count (int): Number of losses of the player
            bet_multiple (int): Multiplier for the bet. It is 2^(loss_count)
            base_bet (int): lowest bet the player makes
    """

    def __init__(self, a_table):
        super().__init__(a_table)
        self.loss_count = 0
        self.bet_multiple = 1
        self.base_bet = a_table.min_limit

    def place_bets(self):
        """Updates the table with a bet on black. The amount bet is bet_multiple"""

        bet_amount = self.base_bet * self.bet_multiple
        if not self.can_place_bet(bet_amount):
            return
        self.table.place_bet(Bet(black, bet_amount))
        self.stake -= bet_amount

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
        return self.stake >= self.bet_multiple * self.base_bet and self.rounds_to_go > 0


class SevenRedsPlayer(MartingalePlayer):
    """A MartingalePlayer who waits until the wheel has spun red seven times in a
    row before betting black. Attrs: red_count (int): Starts at 7, resets to 7
    on each non-red outcome, decrements by 1 on each red outcome.
    """

    def __init__(self, a_table):
        super().__init__(a_table)
        self.red_count = 7

    def place_bets(self):
        """After 7 reds are spun in a row, places a bet on black."""

        if self.red_count == 0:
            super().place_bets()

    def winners(self, outcomes):
        """Notification from the game of all the winning outcomes. If this vector
        includes red, red_count is decremented. Otherwise, red_count is reset to 0.
        Args:
            outcomes (Bin): Winning bin containing outcomes
        """
        includes_red = sum(map(lambda x: x.name == "Red", outcomes.outcomes)) > 0

        if includes_red:
            self.red_count -= 1
        else:
            self.red_count = 7


class RandomPlayer(Player):
    """RandomPlayer is a player who places bets in Roulette. This player makes random bets around the layout.

        Args:
            a_table (Table): The table the player will playing on.

        Attrs:
            rng (Random): A random number generator to generate the next random number.
    """

    def __init__(self, a_table, a_generator):
        super().__init__(a_table)
        self.rng = a_generator

    def set_possible_outcomes(self, outcomes):
        self.possible_outcomes = outcomes

    def _next_bet(self):
        return self.rng.choice(self.possible_outcomes)

    def place_bets(self):
        """Place a randomly selected bet from all possible outcomes and a fixed bet amount."""
        bet_amount = 10
        if not self.can_place_bet(bet_amount):
            return
        outcome = self._next_bet()
        self.table.place_bet(Bet(outcome, bet_amount))
        self.stake -= bet_amount
        return outcome
