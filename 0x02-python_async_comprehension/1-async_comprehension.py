#!/usr/bin/env python3

"""
define async_comprehension
"""
import asyncio
from typing import Generator, List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> Generator[List[float], None, None]:
    """
    return ten random numbers
    """

    result = [await async_generator() for _ in range(10)]

    return result
