#!/usr/bin/env python3

from src.game import Game
from src.player import Passenger57, MartingalePlayer
from src.table import Table
from src.wheel import Wheel
from src.bin_builder import BinBuilder

from test.non_random import NonRandom
import unittest


class TestGame(unittest.TestCase):
    def setUp(self):
        table = Table(200)
        self.player = MartingalePlayer(table)
        self.player.stake = 100
        wheel = Wheel(NonRandom())
        # bin_builder = BinBuilder()
        # bin_builder.build_bins(wheel)
        self.game = Game(wheel, table)

    def test_table(self):
        for i in range(20):
            self.game.cycle(self.player)
            print(self.player.bet_multiple)
            print(self.player.stake)
