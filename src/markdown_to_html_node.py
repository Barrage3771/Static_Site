from markdown_to_blocks import *
from block_to_block_type import *
from textnode import *
from htmlnode import *
from inline_markdown import *
from split_delimiter import*




def header_extraction(text, char_to_count):
    count = 0
    for c in text:
        if c == char_to_count:
            count += 1
        else:
            break
    new = text.replace("#", "")
    new = new.lstrip()
    return count, new

def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    new = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            node = LeafNode(tag='p', value=block)
            new.append(node)
        elif block_type == BlockType.HEADING:
            head = header_extraction(block, "#")
            node = LeafNode(tag=f"h{head[0]}", value=f'{head[1]}')
            new.append(node)
        elif block_type == BlockType.QUOTE:
            
    parent = ParentNode(tag='div', children=new)
    return parent


parent = markdown_to_html_node("""
### THIS IS A HEADER
""")
print(parent.to_html())





