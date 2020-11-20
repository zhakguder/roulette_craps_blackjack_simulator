#!/usr/bin/env python3


class Game:
    def __init__(self, a_wheel, a_table):
        self.the_wheel = a_wheel
        self.the_table = a_table

    def cycle(self, a_player):
        if not a_player.playing():
            return
        a_player.place_bets()
        winning_bin = self.the_wheel.next()
        for bet in self.the_table:
            if bet.outcome in winning_bin.outcomes:
                a_player.win(bet)
            else:
                a_player.lose(bet)
        # I'm not sure if I'm supposed to clean the bets
        self.the_table.bets = []
