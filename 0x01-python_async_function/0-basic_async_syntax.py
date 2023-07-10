#!/usr/bin/env python3

"""
define asynchronous coroutine
"""

import random
import asyncio


async def wait_random(max_delay: float = 10) -> float:
    """
    return random delay value after await
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)

    return delay
