#!/usr/bin/env python3


class Game:
    def __init__(self, a_wheel, a_table):
        self.the_wheel = a_wheel
        self.the_table = a_table

    def cycle(self, a_player):
        """If the player is playing, lets the player place bets, then turns the
        wheel. Notifies the player of the winners and pays off the winning bets."""
        if not a_player.playing():
            return

        a_player.place_bets()
        a_player.set_rounds(a_player.rounds_to_go - 1)
        winning_bin = self.the_wheel.next()
        a_player.winners(winning_bin)
        for bet in self.the_table:
            if bet.outcome in winning_bin.outcomes:
                a_player.win(bet)
            else:
                a_player.lose(bet)
        # I'm not sure if I'm supposed to clean the bets
        self.the_table.bets = []
