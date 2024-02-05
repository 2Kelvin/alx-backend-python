#!/usr/bin/env python3
'''Parameterize and patch as decorators '''
from parameterized import parameterized
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import unittest
from client import GithubOrgClient, _public_repos_url


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

    def test_public_repos_url(self) -> None:
        '''public repos url test'''
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as theOrg:
            theOrg.return_value = {
                'repos_url': 'https://api.github.com/users/google/repos'
            }
            self.assertEqual(
                GithubOrgClient('google')._public_repos_url,
                'https://api.github.com/users/google/repos'
            )


if __name__ == '__main__':
    unittest.main()
