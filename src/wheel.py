#!/usr/bin/env python3
import random
from src.bin_builder import BinBuilder


class Wheel:
    def __init__(self, rng=random.Random()):
        self.bins = 38 * [None]
        BinBuilder().build_bins(self)
        self.rng = rng

    def add_outcome(self, number, outcome):
        """Adds the given outcome to the bin with the given number"""
        self.bins[number].add(outcome)

    def next(self):
        """Picks a random bin"""
        return self.rng.choice(self.bins)

    def get_bin(self, a_bin):
        """Returns the given bin"""
        return self.bins[a_bin]

    def set_bin(self, a_bin, bin):
        """Sets the bin in a_bin position in the bins collection"""
        # if not self.bins[a_bin]:
        self.bins[a_bin] = bin
