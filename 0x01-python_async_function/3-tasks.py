#!/usr/bin/env python3
'''Tasks'''
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int):
    '''Returns asyncio.Task'''
    return asyncio.create_task(wait_random(max_delay))


if __name__ == '__main__':
    task_wait_random()
