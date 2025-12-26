#!/usr/bin/env python3
"""
Unittests for utilities in the ./util.py file
"""
from parameterized import parameterized
import unittest
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """This class contains tests for the
    access_nested_map function
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        This method tests correct input cases
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        This function tests exception cases
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    This class tests the get_json function
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, url, payload):
        """
        This method tests valid input cases
        """
        mock_get_request = Mock()
        mock_get_request.json.return_value = payload

        with patch(
            "utils.requests.get", return_value=mock_get_request
        ) as mock_request:
            self.assertEqual(get_json(url), payload)
            mock_request.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """This class contains tests for the
    Memoize function in utils.py
    """

    def test_memoize(self):
        """
        This function runs tests on the memoize
        function
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        return_value = 42
        with patch.object(
            TestClass, "a_method", return_value=return_value
        ) as mock_req:
            test = TestClass()
            self.assertEqual(test.a_property, return_value)
            self.assertEqual(test.a_property, return_value)
            mock_req.assert_called_once()


if __name__ == "__main__":
    unittest.main()