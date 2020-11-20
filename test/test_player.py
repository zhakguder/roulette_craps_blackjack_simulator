#!/usr/bin/env python3

import unittest
from src.player import MartingalePlayer, SevenRedsPlayer
from src.game import Game
from src.wheel import Wheel
from src.table import Table
from src.bet import Bet
from src.outcome import Outcome
from src.bin import Bin

from test.non_random import NonRandom


class TestMartingalePlayer(unittest.TestCase):
    def setUp(self):

        table = Table(100)
        rng = NonRandom()
        wheel = Wheel(rng)
        self.game = Game(wheel, table)
        self.player = MartingalePlayer(table)
        self.player.stake = 1000
        self.player.rounds_to_go = 10
        self.outcomes = [Outcome("Black", 1), Outcome("Red", 1)]

    def test_bet_multiple(self):
        for i in range(4):
            for i in range(2):
                self.player.win(Bet(self.outcomes[0], self.player.bet_multiple))
                print(self.player.bet_multiple)

            for j in range(3):
                self.player.lose(Bet(self.outcomes[1], self.player.bet_multiple))
                print(self.player.bet_multiple)


class TestSevenRedsPlayer(unittest.TestCase):
    def setUp(self):
        table = Table(100)
        rng = NonRandom()
        wheel = Wheel(rng)
        self.inital_player_stake = 1000
        self.table = table
        self.game = Game(wheel, table)
        self.player = SevenRedsPlayer(table)
        self.player.stake = self.inital_player_stake
        self.player.rounds_to_go = 10
        self.outcomes = Outcome("Black", 1)

    def test_bet_waits(self):
        red = Bin(Outcome("Red", 1))
        black = Bin(Outcome("Black", 1))

        for i in range(7):
            self.player.winners(red)
            self.assertEqual(self.player.stake, self.inital_player_stake)
        self.player.place_bets()
        self.assertEqual(
            self.player.stake, self.inital_player_stake - self.table.min_limit
        )

    def test_bet_multiple(self):
        red = Bin(Outcome("Red", 1))
        black = Bin(Outcome("Black", 1))
        for i in range(4):
            for i in range(2):
                self.player.win(Bet(Outcome("Black", 1), self.player.bet_multiple))
                print(self.player.bet_multiple)

            for j in range(3):
                self.player.lose(Bet(Outcome("Black", 1), self.player.bet_multiple))
                print(self.player.bet_multiple)
