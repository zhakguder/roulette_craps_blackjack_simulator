#!/usr/bin/env python3

from src.outcome import Outcome
from src.bin import Bin


class BinBuilder:
    def build_bins(self, wheel):
        for i in range(0, len(wheel.bins)):
            wheel.set_bin(i, Bin())
        for i in range(1, 37):

            outcome = (self.generate_straight_bet(i),)

            wheel.add_outcome(i, outcome)

        for r in range(0, 12):
            # generate split bets
            first_col_no = 3 * r + 1
            outcome = (self.generate_split_bet(first_col_no, 1),)
            wheel.add_outcome(first_col_no, outcome)
            wheel.add_outcome(first_col_no + 1, outcome)
            second_col_no = 3 * r + 2
            outcome = (self.generate_split_bet(second_col_no, 1),)
            wheel.add_outcome(second_col_no, outcome)
            wheel.add_outcome(second_col_no + 1, outcome)

            # generate street bets
            n = 3 * r + 1
            outcome = (self.generate_street_bet(n),)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)
            wheel.add_outcome(n + 2, outcome)

        for i in range(1, 34):
            # generate split bets
            outcome = (self.generate_split_bet(i, 3),)
            wheel.add_outcome(i, outcome)
            wheel.add_outcome(i + 3, outcome)

        for r in range(0, 11):
            # generate corner bets
            first_col_no = 3 * r + 1
            outcome = (self.generate_corner_bet(first_col_no),)
            wheel.add_outcome(first_col_no, outcome)
            wheel.add_outcome(first_col_no + 1, outcome)
            wheel.add_outcome(first_col_no + 3, outcome)
            wheel.add_outcome(first_col_no + 4, outcome)

            second_col_no = 3 * r + 2
            outcome = (self.generate_corner_bet(second_col_no),)
            wheel.add_outcome(second_col_no, outcome)
            wheel.add_outcome(second_col_no + 1, outcome)
            wheel.add_outcome(second_col_no + 3, outcome)
            wheel.add_outcome(second_col_no + 4, outcome)

            # generate line bets
            n = 3 * r + 1
            outcome = (self.generate_line_bet(n),)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)
            wheel.add_outcome(n + 2, outcome)
            wheel.add_outcome(n + 3, outcome)
            wheel.add_outcome(n + 4, outcome)
            wheel.add_outcome(n + 5, outcome)

        for i in range(0, 3):
            # generate dozen bets
            outcome = (self.generate_dozen_bet(i + 1),)
            for j in range(0, 12):
                wheel.add_outcome(12 * i + j + 1, outcome)
        for i in range(0, 3):
            # generate column bets
            outcome = (self.generate_column_bet(r + 1),)
            for r in range(0, 12):
                wheel.add_outcome(3 * r + i + 1, outcome)

        # generate even money bets
        even_bets = {
            "Red": (self.generate_even_money_bet("Red"),),
            "Black": (self.generate_even_money_bet("Black"),),
            "Even": (self.generate_even_money_bet("Even"),),
            "Odd": (self.generate_even_money_bet("Odd"),),
            "High": (self.generate_even_money_bet("High"),),
            "Low": (self.generate_even_money_bet("Low"),),
        }
        for i in range(1, 37):
            if i < 19:
                wheel.add_outcome(i, even_bets["Low"])
            else:
                wheel.add_outcome(i, even_bets["High"])
            if i % 2 == 0:
                wheel.add_outcome(i, even_bets["Even"])
            else:
                wheel.add_outcome(i, even_bets["Odd"])
            if i in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                wheel.add_outcome(i, even_bets["Red"])
            else:
                wheel.add_outcome(i, even_bets["Black"])

        # generate 0 bets
        five_bet = (Outcome("Five Bet", 6),)
        wheel.add_outcome(0, (self.generate_straight_bet("0"),))
        wheel.add_outcome(0, five_bet)
        wheel.add_outcome(-1, (self.generate_straight_bet("00"),))
        wheel.add_outcome(-1, five_bet)

    def generate_straight_bet(self, n):
        """Generates a straight bet for the given bin
            Args:
                n (int): label of the bin
        """
        n = str(n)
        return Outcome(f"Straight {n}", 35)

    def generate_split_bet(self, n, increment):
        """Generate a split bet for the given bin
            Args:
                n (int): label of the lower bin
                increment (int): difference between two labels
        """
        return Outcome(f"{n}, {n+increment}", 17)

    def generate_street_bet(self, n):
        """Generate a street bet for the given bin
            Args:
                n (int): label of the lowest bin"""
        return Outcome(f"{n}, {n+1}, {n+2}", 11)

    def generate_corner_bet(self, n):
        """Generate a corner bet for the given bin
            Args:
                n (int): label of the lowest bin"""
        return Outcome(f"{n}, {n+1}, {n+3}, {n+4}", 8)

    def generate_line_bet(self, n):
        """Generate a corner bet for the given bin
            Args:
                n (int): label of the lowest bin"""
        return Outcome(f"{n}, {n+1}, {n+2}, {n+3}, {n+4}, {n+5}", 5)

    def generate_dozen_bet(self, n):
        """Generate a dozen bet for the given dozen
            Args:
                n (int): dozen number
        """
        return Outcome(f"Dozen {n}", 2)

    def generate_column_bet(self, n):
        """Generate a column bet for the given column
            Args:
                n (int): column number
        """
        return Outcome(f"Column {n}", 2)

    def generate_even_money_bet(self, name):
        """Generate an even money bet with the given name"""
        return Outcome(name, 1)
