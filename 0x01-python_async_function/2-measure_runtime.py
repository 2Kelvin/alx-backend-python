#!/usr/bin/env python3
'''Measure the runtime'''
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time(n: int, max_delay: int) -> float:
    '''measures execution time of a coroutine'''
    startTime = time.time()

    waitN_coroutine = asyncio.create_task(wait_n(max_delay))
    finishedWaitN = await waitN_coroutine

    endTime = time.time()
    totalTime = endTime - startTime

    return totalTime / n


if __name__ == '__main__':
    asyncio.run(measure_time())
