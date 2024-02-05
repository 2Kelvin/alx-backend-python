#!/usr/bin/env python3
'''Parameterize a unit test'''
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock


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


class TestGetJson(unittest.TestCase):
    '''test get_json'''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        '''test function get_json'''
        props = {"json.return_value": test_payload}
        with patch("requests.get", return_value=Mock(**props)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


if __name__ == '__main__':
    unittest.main()
