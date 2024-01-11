#!/usr/bin/env python3
'''Annotated mixed list'''
from typing import List, Union


def sum_mixed_list(mxd_list: List[Union[int, float]]) -> float:
    '''Adds up all the floats & ints in the list'''
    return sum(mxd_list)
