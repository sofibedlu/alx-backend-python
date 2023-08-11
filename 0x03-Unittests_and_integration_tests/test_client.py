#!/usr/bin/env python3
"""Test case for client Module"""

from fixtures import TEST_PAYLOAD
import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import (
        patch,
        MagicMock,
        PropertyMock,
        Mock
        )


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class methods"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test the org method of GithubOrgClient."""
        url_repos = "https://api.github.com/orgs/{}/repos"
        mock_get_json.return_value = {"repos_url": url_repos.format(org_name)}

        client_instance = GithubOrgClient(org_name)
        org_data = client_instance.org

        self.assertEqual(org_data["repos_url"], url_repos.format(org_name))

        url = "https://api.github.com/orgs/{}"
        mock_get_json.assert_called_once_with(url.format(org_name))

    def test_public_repos_url(self):
        """
        Test the _public_repos_url property of GithubOrgClient.

        The test uses the unittest.mock.patch context manager to mock the
        behavior of the org method, ensuring a known payload is returned.
        It then creates an instance of GithubOrgClient, accesses
        the _public_repos_url property, and compares it with the expected
        URL based on the mocked payload.
        """
        org_name = "abc"
        expected_url = 'https://api.github.com/orgs/{}/repos'.format(org_name)

        # Create a mock instance of GithubOrgClient and mock the
        # property using PropertyMock
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}

            client_instance = GithubOrgClient(org_name)
            public_repos_url = client_instance._public_repos_url

            self.assertEqual(public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient.
        """
        org_name = "abc"
        expected_repos = [
                {"name": "repo1"},
                {"name": "repo2"},
                {"name": "repo3"}]

        mock_get_json.return_value = expected_repos

        # Mock the property _public_repos_url to return a known value
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_property:
            mock_property.return_value = 'https://api.github.com/repos'

            client_instance = GithubOrgClient(org_name)
            repos = client_instance.public_repos()

            self.assertEqual(repos, [repo["name"] for repo in expected_repos])

            mock_property.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test the has_license method of GithubOrgClient.
        """
        client_instance = GithubOrgClient("abc")
        result = client_instance.has_license(repo, license_key)

        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration Test case for GithubOrgClient class methods
    """
    @classmethod
    def setUpClass(cls):
        """Set up the integration test environment"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define the side_effect for requests.get to return payloads

        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Clean up the integration test environment"""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """
        Test the public_repos method of GithubOrgClient in an integration test.
        """
        org_name = "abc"
        client_instance = GithubOrgClient(org_name)
        repos = client_instance.public_repos()

        self.assertEqual(repos, self.expected_repos)
        self.mock_get.assert_called_with(self.org_payload["repos_url"])
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos(self):
        """Tests the public_repos method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self):
        """Tests the public_repos method with a license filter."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
