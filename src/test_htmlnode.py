import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "http://example.com", "rel": "nofollow"})
        expected = ' href="http://example.com" rel="nofollow"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        node = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(None, None, None, {"class": "main"})
        self.assertEqual(node.props_to_html(), ' class="main"')