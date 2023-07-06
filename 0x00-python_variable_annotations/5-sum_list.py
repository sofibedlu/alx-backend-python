#!/usr/bin/env python3

"""
define sum_liat type-annotated function
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """return sum of list of float item
    """
    result = 0
    for elem in input_list:
        result += elem
    return result
