#!/usr/bin/env python3
'''The basics of async'''
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    '''returns a random float'''
    delay = random.uniform(float(0), float(max_delay))
    return delay


if __name__ == '__main__':
    asyncio.run(wait_random())