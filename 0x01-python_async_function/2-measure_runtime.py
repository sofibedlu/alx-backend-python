#!/usr/bin/env python3

"""
define measure_time
"""
import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    measure an approximate elasped time
    """
    start_time = time.time()

    async def run_wait_n():
        await wait_n(n, max_delay)

    asyncio.run(run_wait_n())

    time_elapsed = time.time() - start_time

    return time_elapsed / n
