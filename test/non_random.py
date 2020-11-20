#!/usr/bin/env python3

import random


class NonRandom(random.Random):
    """Non random number generator for testing only."""

    def __init__(self, seed=0):
        super().__init__()
        self.value = -1

    def random(self):
        self.value += 1
        return (self.value % 38) / 38
