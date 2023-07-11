#!/usr/bin/env python3

"""
define async_comprehension
"""
import asyncio
from typing import Generator, List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    return ten random numbers
    """

    result = [num async for num in async_generator()]

    return result
