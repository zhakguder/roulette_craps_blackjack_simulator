#!/usr/bin/env python3

from src.game import Game
from src.player import MartingalePlayer, SevenRedsPlayer
from src.simulator import Simulator
from src.table import Table
from src.wheel import Wheel

from test.non_random import NonRandom

wheel = Wheel()
table = Table(1000)
game = Game(wheel, table)
player = SevenRedsPlayer(table)
simulator = Simulator(game, player)

# possible_outcomes = []
# for bin in wheel.bin_iterator():
#     for outcome in bin:
#         possible_outcomes.append(outcome)
# self.player.set_possible_outcomes(possible_outcomes)

simulator.gather()
print(simulator.durations)
print(simulator.maxima)
