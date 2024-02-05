#!/usr/bin/env python3
'''Parameterize a unit test'''
import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Dict, Tuple, Union


class TestAccessNestedMap(unittest.TestCase):
    '''access_nested_map test class'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple[str],
                               answer: Union[Dict, int]) -> None:
        '''testing function access_nested_map'''
        self.assertEqual(access_nested_map(nested_map, path), answer)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self, nested_map: Dict, path: Tuple[str],
            errRaised: Exception) -> None:
        '''tests key error'''
        with self.assertRaises(errRaised):
            access_nested_map(nested_map, path)


if __name__ == '__main__':
    unittest.main()
