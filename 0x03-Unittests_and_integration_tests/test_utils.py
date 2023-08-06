#!/usr/bin/env python3
"""
define a TestAccessNestedMap class
"""
import requests
import unittest
from utils import access_nested_map, memoize
from parameterized import parameterized
from typing import Sequence, Mapping, Any, Dict
from unittest.mock import Mock
from unittest.mock import patch
from utils import get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function in utils module."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected: Any
            ) -> None:
        """Test the access_nested_map function."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"),),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence
            ) -> None:
        """Test that KeyError is raised for specific inputs"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test case for the get_json function in utils module."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, url: str, data: Dict):
        """Test the get_json function."""
        mock_response = Mock()
        mock_response.json.return_value = data

        with unittest.mock.patch("requests.get", return_value=mock_response):
            result = get_json(url)

        self.assertEqual(result, data)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator and its application.
    """
    def test_memoize(self) -> None:
        """Test the memoization behavior of a memoized property.
        """
        class TestClass:
            """sample tes class"""
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42

            obj = TestClass()

            result1 = obj.a_property
            result2 = obj.a_property

            mock_a_method.assert_called_once()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
