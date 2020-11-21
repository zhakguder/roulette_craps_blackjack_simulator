#!/usr/bin/env python3
import math


def mean(a_list):
    """Computes the mean of integers in a_list"""
    return sum(a_list) / len(a_list)


def stdev(a_list):
    list_mean = mean(a_list)
    n_list = len(a_list)
    variance = sum(map(lambda x: math.pow(x - list_mean, 2), a_list)) / (n_list - 1)
    return math.sqrt(variance)
