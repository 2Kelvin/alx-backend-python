#!/usr/bin/env python3
'''Annotated string & int/float to tuple'''
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''Turns arguments passed in into "k", v tuple values'''
    return (k, (v*v))
