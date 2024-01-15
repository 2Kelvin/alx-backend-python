#!/usr/bin/env python3
'''Tasks'''
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''spawns wait_random delayed time n times'''
    floatArray: List[float] = []

    for _ in range(n):
        floatArray.append(await task_wait_random(max_delay))

    return sorted(floatArray)


if __name__ == '__main__':
    asyncio.run(task_wait_n())
