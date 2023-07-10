#!/usr/bin/env python3

"""
define async routine wait_n
"""
import asyncio
import queue
from typing import List
from asyncio import Task


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    it spawn wait_random n times with the specified
    max_delay
    """

    delays = queue.PriorityQueue()

    async def handle_task(task: Task):
        delay: float = await task
        delays.put(delay)

    tasks = [wait_random(max_delay) for _ in range(n)]
    await asyncio.gather(*(handle_task(task) for task in tasks))

    ordered_delays: List[float] = []
    while not delays.empty():
        ordered_delays.append(delays.get())

    return ordered_delays
