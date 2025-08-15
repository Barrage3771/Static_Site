from markdown_to_blocks import *
from block_to_block_type import *
from textnode import *
from htmlnode import *
from inline_markdown import *
from split_delimiter import*




def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    for block in blocks:
        result = block_to_block_type(block)
        node = text_node_to_html_node(result)
        node.LeafNode.to_html()
        