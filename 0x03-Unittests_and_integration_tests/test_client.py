#!/usr/bin/env python3
"""Test case for client Module"""

import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class methods"""

    @parameterized.expand([
        ("google"),
        ("abc")
        ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Test the org method of GithubOrgClient."""
        client = GithubOrgClient(org_name)
        url_repos = "https://api.github.com/orgs/{}/repos"
        mock_get_json.return_value = {"repos_url": url_repos.format(org_name)}

        org_data = client.org

        self.assertEqual(org_data["repos_url"], url_repos.format(org_name))

        url = "https://api.github.com/orgs/{}"
        mock_get_json.assert_called_once_with(url.format(org_name))
