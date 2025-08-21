import unittest
from text_to_textnodes import *

class TestTextNodeFunction(unittest.TestCase):
    def test_text_to_textnodes_basic(self):
        text = "Hello **bold** and _italic_ plus `code` and ![alt](image.png) plus [Boot](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" plus ", TextType.TEXT),
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

    def test_only_image_and_links(self):
        text = "![image](image.png) plus [boot](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("image", TextType.IMAGE, "image.png"),
            TextNode(" plus ", TextType.TEXT),
            TextNode("boot", TextType.LINK, "https://boot.dev"),
        ]

    def test_consecutive_markdown(self):
        text = "This is **bold****bold** text."
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]

    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        assert nodes == []