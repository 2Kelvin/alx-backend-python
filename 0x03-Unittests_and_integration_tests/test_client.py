#!/usr/bin/env python3
'''Parameterize and patch as decorators '''
from parameterized import parameterized, parameterized_class
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import unittest
from client import GithubOrgClient, _public_repos_url, has_license
from fixtures import TEST_PAYLOAD
from requests import HTTPError


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
        """test public repos url"""
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
        mock_get_json.return_value = test_payload["repos"]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
        ) as mockedRepoUrl:
            mockedRepoUrl.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mockedRepoUrl.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ("lic_true", {"license": {"key": "my_license"}},
         "my_license", True),
        ("lic_false", {"license": {"key": "other_license"}},
         "my_license", False)
    ])
    def test_has_license(self, repo: Dict, key: str, answer: bool) -> None:
        '''unit test for has_license'''
        githubClnt = GithubOrgClient('google')
        boolHasLicence = githubClnt.has_license(repo, key)
        self.assertEqual(boolHasLicence, answer)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''class to test Github client Integration'''

    @classmethod
    def setUpClass(cls) -> None:
        '''the setup class'''
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            '''fetch the payload'''
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError
        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        '''test method public repos'''
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        '''test public repos with a license'''
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        '''the  teardown class method'''
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
