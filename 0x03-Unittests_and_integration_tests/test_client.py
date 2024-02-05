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
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as theOrg:
            theOrg.return_value = {
                'repos_url': 'https://api.github.com/users/google/repos'
            }
            self.assertEqual(
                GithubOrgClient('google')._public_repos_url,
                'https://api.github.com/users/google/repos'
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        '''test public_repos'''
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload['repos']
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mockUrl:
            mockUrl.return_value = test_payload['repos_url']
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                ['episodes.dart', 'kratu']
            )
            mockUrl.assert_called_once()
        mock_get_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
