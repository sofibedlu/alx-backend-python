#!/usr/bin/env python3
"""
define typed annotated function to_kv
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    return a tuble
    """
    return (k, v * v)
