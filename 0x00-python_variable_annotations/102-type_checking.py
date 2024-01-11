#!/usr/bin/env python3
'''More involved type annotations'''


def zoom_array(lst: list, factor: int = 2) -> list:
    '''fixed all annotaion issues with this function using mypy'''
    zoomed_in: list = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = [12, 72, 91]

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
