#!/usr/bin/env python3
"""
define a TestAccessNestedMap class
"""

import unittest
from utils import access_nested_map
from parameterized import parameterized
from typing import Sequence, Mapping, Any


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
