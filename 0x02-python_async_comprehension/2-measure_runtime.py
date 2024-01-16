#!/usr/bin/env python3
'''Run time for four parallel comprehensions'''
import time
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''Measures & returns async_comprehension total runtime'''
    startTime = time.time()

    coroutinesArr = []

    for _ in range(4):
        eachCoroutineTask = asyncio.create_task(async_comprehension())
        coroutinesArr.append(eachCoroutineTask)

    await asyncio.gather(*coroutinesArr)

    endTime = time.time()

    return endTime - startTime
