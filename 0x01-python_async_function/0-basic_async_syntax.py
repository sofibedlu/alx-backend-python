#!/usr/bin/env python3

"""
define asynchronous coroutine that takes in an integer argument
named wait_random that waits for seconds and eventually returns it.
"""

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """
    return random delay value after await
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)

    return delay
