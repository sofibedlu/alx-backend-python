#!/usr/bin/env python3

"""
define type-annotated function make_multiplier
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    return a function
    """
    return (lambda number: number * multiplier)
