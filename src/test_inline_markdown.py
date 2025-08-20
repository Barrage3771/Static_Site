import unittest

from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_empty_split_images(self):
        node = TextNode(
            "This is a text with no image at all.",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is a text with no image at all.", TextType.TEXT)],
            new_nodes
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](www.example.com) and another [secondlink](www.anotherexample.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ",TextType.TEXT),
                TextNode("link", TextType.LINK, "www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("secondlink", TextType.LINK, "www.anotherexample.com")
            ],
            new_nodes
        )
        
    def test_empty_links(self):
        node = TextNode(
            "This is a text with no link at all.",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is a text with no link at all.", TextType.TEXT)],
            new_nodes
        )
        