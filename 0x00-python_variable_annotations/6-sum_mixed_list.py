#!/usr/bin/env python3

"""
define sum_mixed_list type annotated function
"""
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    return sum of list
    """
    result = 0
    for ele in mxd_lst:
        result += ele

    return result
