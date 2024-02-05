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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Method to unit test GithubOrgClient.public_repos
        """
        mock_url = "https://api.github.com/orgs/google/repos"
        payload = {mock_url: [{"name": "google/episodes.dart", "license": {
            "key": "bsd-3-clause",
            "name": "BSD 3-Clause \"New\" or \"Revised\" License",
            "spdx_id": "BSD-3-Clause",
            "url": "https://api.github.com/licenses/bsd-3-clause",
            "node_id": "MDc6TGljZW5zZTU="
        }}, {"name": "cpp-netlib", "license": None},
            {"name": "ios-webkit-debug-proxy"}]}
        mock_get_json.return_value = payload[mock_url]
        with patch('test_client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repo:
            mock_public_repo.return_value = mock_url
            gitcli = GithubOrgClient("google")
            names_list = gitcli.public_repos()
            expected_list = ["google/episodes.dart",
                             "cpp-netlib", "ios-webkit-debug-proxy"]
            self.assertEqual(names_list, expected_list)
            mock_public_repo.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
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
