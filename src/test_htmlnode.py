import unittest

from htmlnode import *
from split_delimiter import *

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

# LEAF NODE #

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_empty_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_different_tag(self):
        node = LeafNode("h1", "This is a heading")
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")

    def test_leaf_multiple_props(self):
        node = LeafNode("input", "Button", {"type": "button", "value": "Click", "disabled": "true"})
        self.assertEqual(node.to_html(), '<input type="button" value="Click" disabled="true">Button</input>')

    
# PARENT NODE #
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_multiple_children(self):
        child1 = LeafNode("span", "first child")
        child2 = LeafNode("i", "second child")
        child3 = LeafNode("u", "third child")
        
        parent_node = ParentNode("div", [child1, child2, child3])
        
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first child</span><i>second child</i><u>third child</u></div>"
        )
    
    def test_empty_child(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(),
            "<div></div>"
        )
        
    def test_no_child(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    def test_no_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_mixed_child_types(self):
    # Test parent with mix of LeafNode and ParentNode children
        leaf1 = LeafNode("b", "bold")
        parent_child = ParentNode("span", [LeafNode("i", "italic")])
        leaf2 = LeafNode("u", "underline")
        
        parent_node = ParentNode("div", [leaf1, parent_child, leaf2])
        
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>bold</b><span><i>italic</i></span><u>underline</u></div>"
        )

    def test_leaf_and_parent_nodes_mixed(self):
        # Test parent with LeafNode without tag and other node types
        text_node = LeafNode(None, "Just text")
        regular_node = LeafNode("span", "In span")
        
        parent_node = ParentNode("p", [text_node, regular_node, text_node])
        
        self.assertEqual(
            parent_node.to_html(),
            "<p>Just text<span>In span</span>Just text</p>"
        )
        
    def test_parent_with_props(self):
        # Test that props render correctly in a parent node
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )
        
# TEXT NODE #

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")
        
    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")
    
    def test_link(self):
        node = TextNode("anchor text", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.props, {"href": "google.com"})
        
    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "example.com", "alt": "Alt text"})
        
# DELIMITER TESTS #

    def test_multiple_delims(self):
        node = TextNode("This has **bold**, and `code`.", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        step2 = split_nodes_delimiter(step1, "`", TextType.CODE)
        self.assertEqual(
            step1,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", and `code`.", TextType.TEXT),
            ]
        )
        
        self.assertEqual(
            step2,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT)
            ]
        )
        
    
    def test_italic_bold_delims(self):
        node = TextNode("This is __italic__ and **bold** text.", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "__", TextType.ITALIC)
        step2 = split_nodes_delimiter(step1, "**", TextType.BOLD)
        self.assertEqual(
            step1,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and **bold** text.", TextType.TEXT)
            ]
        )
        
        self.assertEqual(
            step2,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT)
            ]
        )
        
    def test_three_delims(self):
        node = TextNode("This is a __italic__ with **bold** also including `code` text.", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "__", TextType.ITALIC)
        step2 = split_nodes_delimiter(step1, "**", TextType.BOLD)
        step3 = split_nodes_delimiter(step2, "`", TextType.CODE)
        self.assertEqual(
            step1,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with **bold** also including `code` text.", TextType.TEXT)
            ]
        )
        
        self.assertEqual(
            step2,
            [
               TextNode("This is a ", TextType.TEXT),
               TextNode("italic", TextType.ITALIC),
               TextNode(" with ", TextType.TEXT),
               TextNode("bold", TextType.BOLD),
               TextNode(" also including `code` text.", TextType.TEXT)
            ]
        )
        
        self.assertEqual(
            step3,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" also including ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text.", TextType.TEXT)
            ]
        )
    
    def test_no_closing_delims(self):
        node = TextNode("This is a broken **bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
            
    def test_same_multiple_delims(self):
        node = TextNode("This is **multiple** types of **bold** characters", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            step1,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("multiple", TextType.BOLD),
                TextNode(" types of ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" characters", TextType.TEXT)
            ]
        )
        
    def test_empty_delim(self):
        node = TextNode("This is a **** empty bold", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            step1,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("", TextType.BOLD),
                TextNode(" empty bold", TextType.TEXT)
            ]
        )


    #RegEx tests

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_no_match_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is a text with no image or link"
        )
        self.assertListEqual([], matches)
    
    def test_multiple_matches_extract(self):
        matches = extract_markdown_images(
            "This is a text with ![image](https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg) and also this ![image](https://upload.wikimedia.org/wikipedia/commons/9/9e/Ours_brun_parcanimalierpyrenees_1.jpg)"
        )
        expected_matches = [
            ("image", "https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg"),
            ("image", "https://upload.wikimedia.org/wikipedia/commons/9/9e/Ours_brun_parcanimalierpyrenees_1.jpg")
        ]
        self.assertListEqual(expected_matches, matches)
        
    def test_mixed_content(self):
        text_with_mixed_content = "This is text with ![image](https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg) also it has [link](https://www.example.com) with a ![picture](https://imgur.com/gallery/grenc-rKXI4zf#/t/goofy)"
        match1 = extract_markdown_images(text_with_mixed_content)
        match2 = extract_markdown_links(text_with_mixed_content)
        
        expected_matches1 = [
            ("image", "https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg"),
            ("picture", "https://imgur.com/gallery/grenc-rKXI4zf#/t/goofy")
        ]
        
        expected_matches2 = [
            ("link", "https://www.example.com")
        ]
        
        self.assertListEqual(expected_matches1, match1)
        self.assertListEqual(expected_matches2, match2)
        
    def test_edge_case_extract(self):
        text_edge_case = "![image](https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg) this is a edge case test same with this ![image](https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg)"
        
        matches = extract_markdown_images(text_edge_case)
        
        expected_match = [
            ("image", "https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg"),
            ("image", "https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg")
        ]
        
        self.assertListEqual(expected_match, matches)
        
    def test_empty_alt_url(self):
        text_empty = "This is text with empty alt and url ![]()"
        
        matches = extract_markdown_images(text_empty)
        
        self.assertListEqual([("", "")], matches)