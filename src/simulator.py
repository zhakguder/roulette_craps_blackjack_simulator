#!/usr/bin/env python3


class Simulator:
    """Simulator runs the Roulette game simulation with a given player placing bets.
    It reports raw statistics on a number of sessions of play.

        Attrs:
            init_duration (int): Number of game cycles player has patience for.
            init_stake (int): Amount of money each player will have at the beginning of each simulation cycle.
            samples (int): Number of simulation cycles.
            durations (list): A list of lengths of time the player remained in the game. Each session of play produces a duration metric, which are collected in this list.
            maxima (list): A list of maximum stakes for each player. Each session of play produces a maximum stake metric, which are collected into this list.
            player (Player): The betting strategy we are simulating.
            game (Game): The casino game we are simulating.

    """

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.init_duration = 250
        self.init_stake = 100
        self.samples = 50
        self.durations = []
        self.maxima = []

    def session(self):
        """Executes a single game session. Initializes the player with initial stake and
        initial cycles. Executes the game cycle for the duration of the session.
        Returns:
            stake_values (list): The list of individual stake values after each game cycle.
        """
        self.player.set_stake(self.init_stake)
        self.player.set_rounds(self.init_duration)

        stake_values = []
        while self.player.playing():
            self.game.cycle(self.player)
            stake_values.append(self.player.stake)
        self.player.bet_multiple = 1
        return stake_values

    def gather(self):
        """Executes the number of samples sessions."""

        # For each game session
        for i in range(self.samples):
            # simulate the session
            stake_values = self.session()
            # keep the duration of the session
            self.durations.append(len(stake_values))
            # and the maximum stake during the session
            self.maxima.append(max(stake_values))
