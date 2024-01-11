#!/usr/bin/env python3
'''Complex annotated functions'''
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''Function returns another functions that takes in a float'''

    def myFunc(x: float) -> float:
        '''Takes in a float & multiplies it witha multiplier'''
        return x * multiplier

    return myFunc
