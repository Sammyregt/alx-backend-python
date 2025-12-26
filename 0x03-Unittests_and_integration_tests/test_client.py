#!/usr/bin/env python3
"""
Test Client
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    This class contains tests for the
    GithubOrgClient class
    """
    @parameterized.expand([("google",), ("abc",)])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        This method tests the org method of
        the GithubOrgClient class
        """
        expected_value = {"org": org_name}
        mock_get_json.return_value = expected_value

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_value)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        This method tests the _public_repos_url
        property method
        """
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_pub_repo_return_value = "https://test.com"
            mock_public_repos_url.return_value = mock_pub_repo_return_value

            client = GithubOrgClient('test')
            result = client._public_repos_url

            self.assertEqual(result, mock_pub_repo_return_value)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        This method tests the public_repos method
        """
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_pub_repo_return_val = "https://test.com"
            mock_get_json_return_val = [
                {"name": "repo1", "url": "https://test1.com"},
                {"name": "repo2", "url": "https://test2.com"}
            ]
            mock_public_repos_url.return_value = mock_pub_repo_return_val
            mock_get_json.return_value = mock_get_json_return_val

            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license"),
        ({"license": {"key": "other_license"}}, "other_license")
    ])
    def test_has_license(self, repo, license_key):
        """
        This function tests the has license function
        """
        client = GithubOrgClient('test')
        self.assertTrue(client.has_license(repo, license_key))


@parameterized_class(
    [
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set up side_effect"""
        cls.get_patcher = patch('requests.get', side_effect=cls.side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def side_effect(cls, url, *args, **kwargs):
        """Side effect function for requests.get mock."""
        if url == "https://api.github.com/orgs/google":
            return Mock(
                status_code=200,
                json=MagicMock(return_value=cls.org_payload),
            )
        if url == "https://api.github.com/orgs/google/repos":
            return Mock(
                status_code=200,
                json=MagicMock(return_value=cls.repos_payload),
            )
        raise ValueError(f"Unmocked url: {url}")

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by license"""
        client = GithubOrgClient("google")
        apache_repos = client.public_repos(license="apache-2.0")

        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()