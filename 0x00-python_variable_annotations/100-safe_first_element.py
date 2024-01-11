#!/usr/bin/env python3
'''Duck typing - first element of a sequence'''
from typing import Sequence, Any, Union


# The types of the elements of the input are not known
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''returns a sequence's first item or none if empty'''
    if lst:
        return lst[0]
    else:
        return None
