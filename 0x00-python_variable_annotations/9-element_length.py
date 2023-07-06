#!/usr/bin/env python3
"""
define type-annotated function element_length
"""

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """return list of tuples
    """

    return [(i, len(i)) for i in lst]
