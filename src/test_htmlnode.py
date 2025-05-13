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
