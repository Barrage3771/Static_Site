from htmlnode import *
from textnode import *
from inline_markdown import *
from split_delimiter import *

def text_to_textnodes(text):
    new_nodes = []
    delimiters = [
        ("**", TextType.BOLD),
        ("__", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("*", TextType.ITALIC),
        ("`", TextType.CODE),
    ]
    node = TextNode(text, TextType.TEXT)
    curr_nodes = [node]
    for delimiter, text_type in delimiters:
        curr_nodes = split_nodes_delimiter(curr_nodes, delimiter, text_type)
    curr_nodes = split_nodes_link(curr_nodes)
    curr_nodes = split_nodes_image(curr_nodes)
    return curr_nodes