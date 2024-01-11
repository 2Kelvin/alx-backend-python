#!/usr/bin/env python3
'''Duck typing'''
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''Function returns a tuple of elements' length'''
    return [(i, len(i)) for i in lst]
