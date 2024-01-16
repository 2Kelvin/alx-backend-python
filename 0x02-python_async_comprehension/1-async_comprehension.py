#!/usr/bin/env python3
async_generator = __import__('0-async_generator').async_generator
from typing import List


async def async_comprehension() -> List[float]:
    '''Collects and returns 10 random numbers'''
    return [eachFloat async for eachFloat in async_generator()]


if __name__ == '__main__':
    async_comprehension()
