import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_texttype_not(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_two_urls_dif(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.bootdev.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()