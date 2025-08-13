import unittest
from text_to_textnodes import *

class TestTextNodeFunction(unittest.TestCase):
    def test_text_to_textnodes_basic(self):
        text = "Hello **bold** and _italic_ plus `code` and ![alt](image.png) plus [Boot](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and _italic_ plus ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image.png"),
            TextNode(" plus ", TextType.TEXT),
            TextNode("Boot", TextType.LINK, "https://boot.dev"),
        ]

    def test_text_to_textnodes_plain(self):
        text = "Plain text only, no markdown!"
        nodes = text_to_textnodes(text)
        assert nodes == [TextNode("Plain text only, no markdown!", TextType.TEXT)]