#!/usr/bin/env python3
'''Parameterize and patch as decorators '''
from parameterized import parameterized
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock, MagicMock
import unittest
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''TestGithubOrgClient class'''

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, theResponse: Dict, mocked: MagicMock) -> None:
        '''test for GithubOrgClient'''
        mocked.return_value = MagicMock(return_value=theResponse)
        githubClient = GithubOrgClient(org)
        self.assertEqual(githubClient.org(), theResponse)
        mocked.assert_called_once_with(f'https://api.github.com/orgs/{org}')


if __name__ == '__main__':
    unittest.main()
