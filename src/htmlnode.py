import re
from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        new_string = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            new_string += " " + key + "=" + '"' + value + '"'
        return new_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.value is None or self.value == '':
            if self.tag in ["img", "br", "hr"]:
                props_html = self.props_to_html()
                return f"<{self.tag}{props_html} />"
            else:
                raise ValueError("LeafNode must have value")
        elif self.tag is None:
            return f"{self.value}"

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode missing tag")
        if self.children is None:
            raise ValueError("ParentNode missing children")
        html = f"<{self.tag}"
        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        html += ">"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)