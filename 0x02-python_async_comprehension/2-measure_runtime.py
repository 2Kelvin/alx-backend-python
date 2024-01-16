#!/usr/bin/env python3
'''Run time for four parallel comprehensions'''
import time
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''Measures & returns async_comprehension total runtime'''
    startTime = time.time()

    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    endTime = time.time()

    return endTime - startTime
