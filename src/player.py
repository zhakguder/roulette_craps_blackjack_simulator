#!/usr/bin/env python3
from src.outcome import Outcome
from src.bet import Bet
from math import pow

from src.player_states import (
    Player1326NoWins,
    Player1326OneWin,
    Player1326TwoWins,
    Player1326ThreeWins,
)


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
        self.base_bet = a_table.min_limit

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

    def reset(self):
        self.bet_multiple = 1


class Passenger57(Player):
    def __init__(self, a_table):
        super().__init__(a_table)

    def place_bets(self):
        bet_amount = self.base_bet
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

    outcome = Outcome("Black", 1)

    def __init__(self, a_table):
        super().__init__(a_table)
        self.loss_count = 0
        self.bet_multiple = 1

    def place_bets(self):
        """Updates the table with a bet on black. The amount bet is bet_multiple"""

        bet_amount = self.base_bet * self.bet_multiple
        if not self.can_place_bet(bet_amount):
            return
        self.table.place_bet(Bet(MartingalePlayer.outcome, bet_amount))
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

    def _next_outcome(self):
        return self.rng.choice(self.possible_outcomes)

    def place_bets(self):
        """Place a randomly selected bet from all possible outcomes and a fixed bet amount."""
        bet_amount = self.base_bet
        if not self.can_place_bet(bet_amount):
            return
        outcome = self._next_outcome()
        self.table.place_bet(Bet(outcome, bet_amount))
        self.stake -= bet_amount
        return outcome


class Player1326(Player):
    """Player1326 follows the 1-3-2-6 betting system. The player has a preferred
    Outcome, can be any even money bet. The player also has a current betting state
    that determines the current bet to place, and what next state applies when the bet has won or lost.

    Attrs: state (Player1326State): Current state of the 1-3-2-6 betting system.
        It can be one of Player1326NoWins, Player1326OneWin, Player1326TwoWins,
        Player1326ThreeWins
    """

    def __init__(self, a_table):
        super().__init__(a_table)
        self.state = Player1326NoWins(self)
        self.outcome = Outcome("Black", 1)

    def place_bets(self):
        """Updates the table with a bet created by the current state. This method
        delegates the bet creation to the current state."""
        bet = self.state.current_bet()
        if not self.stake >= bet.amount:
            return False
        self.table.place_bet(bet)
        self.stake -= bet.amount

    def win(self, bet):
        """Superclass method updates the player's stake with the amount won. User's state is updated."""
        super().win(bet)
        self.state = self.state.next_won()

    def lose(self, bet):
        """User's state is updated."""
        self.state = self.state.next_loss()

    def playing(self):
        bet = self.state.current_bet()
        return self.stake >= bet.amount and self.rounds_to_go > 0

    def reset(self):
        self.state = Player1326NoWins(self)


class PlayerCancellation(Player):
    """PlayerCancellation usese the cancellation betting system. Bets on even money
    Outcomes. This implementation uses Black.

    Attrs:

        sequence (list): Keeps the bet amounts. Wins are removed from this
        list and losses are appended to this list. The current bet is the first
        value plus the last value.

        outcome (Outcome): This is the player's preferred outcome.
    """

    def __init__(self, a_table):
        super().__init__(a_table)
        self.outcome = Outcome("Black", 1)
        self.reset()

    def reset(self):
        """Puts the list of first six integers into the sequence variable"""
        self.sequence = list(range(1, 7))

    def place_bets(self):
        """Creates a bet from the sum of the first and last values of sequence. The
        first value is at index 0."""
        bet_amount = self.bet_amount()
        bet = Bet(self.outcome, bet_amount)
        if not self.stake >= bet.amount:
            return False
        self.table.place_bet(bet)
        self.stake -= bet.amount

    def bet_amount(self):
        return self.base_bet * (self.sequence[0] + self.sequence[-1])

    def win(self, bet):
        """Updates the player stake with the amount won. Removes the first and the last
        number from the sequence."""
        super().win(bet)
        self.sequence = self.sequence[1:-1]

    def lose(self, bet):
        """Appends the sum of the first and list elements of sequence to the end of sequence as a new integer."""
        last_entry = self.sequence[0] + self.sequence[-1]
        self.sequence.append(last_entry)

    def playing(self):
        """Player keeps playing until the sequence is empty or he doesn't have enough
        money or no more rounds left to go in the game."""
        if not self.sequence:
            return False
        return self.stake >= self.bet_amount() and self.rounds_to_go > 0


class PlayerFibonacci(Player):
    """This player uses the Fibonacci sequence to structure a series of bets in a kind of cancellation system.
        Attrs:
            recent (int): The most recent bet multiplier
            previoius (int): The bet multiplier previous to the most recent bet amount
    """

    def __init__(self, a_table):
        super().__init__(a_table)
        self.reset()
        self.outcome = Outcome("Black", 1)

    def place_bets(self):
        """Creates a bet from the sum of the first and last values of sequence. The
        first value is at index 0."""
        bet_amount = self.bet_amount()
        bet = Bet(self.outcome, bet_amount)

        self.table.place_bet(bet)
        self.stake -= bet.amount

    def bet_amount(self):
        return self.base_bet * (self.previous + self.recent)

    def win(self, bet):
        super().win(bet)
        if self.previous == 0:
            return
        new_previous = self.recent - self.previous
        self.recent = self.previous
        self.previous = new_previous

    def lose(self, bet):
        new_recent = self.recent + self.previous
        self.previous = self.recent
        self.recent = new_recent

    def playing(self):
        return self.stake >= self.bet_amount() and self.rounds_to_go > 0

    def reset(self):
        self.recent = 1
        self.previous = 0
