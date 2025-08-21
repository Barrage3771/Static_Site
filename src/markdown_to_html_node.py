from markdown_to_blocks import *
from block_to_block_type import *
from textnode import *
from htmlnode import *
from inline_markdown import *
from split_delimiter import *
from text_to_textnodes import *

#code
#link
#image
#italics
#bold

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
            textnodes = text_to_textnodes(block)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            node = ParentNode(tag="p", children=children)
            new.append(node)
        elif block_type == BlockType.HEADING:
            head = header_extraction(block, "#")
            textnodes = text_to_textnodes(head[1])
            children = [text_node_to_html_node(tn) for tn in textnodes]
            node = ParentNode(tag=f"h{head[0]}", children=children)
            new.append(node)
        elif block_type == BlockType.QUOTE:
            content = block[2:]
            content = content.lstrip() # all white space preceding the text is taken out
            textnodes = text_to_textnodes(content)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            node = ParentNode(tag="blockquote", children=children)
            new.append(node)
        elif block_type == BlockType.UNORDERED: #ul
            lines = block.split('\n')
            li_nodes = []
            for line in lines:
                if line.strip():
                    content = line.lstrip("- ").lstrip()
                    textnodes = text_to_textnodes(content)
                    children = [text_node_to_html_node(tn) for tn in textnodes]
                    li_node = (ParentNode(tag="li", children=children))
                    li_nodes.append(li_node)
            node = ParentNode(tag="ul", children=li_nodes)
            new.append(node)
        elif block_type == BlockType.ORDERED:
            lines = block.split('\n')
            li_nodes = []
            for line in lines:
                if line.strip():
                    content = line.split(".", 1)[1].lstrip()
                    textnodes = text_to_textnodes(content)
                    children = [text_node_to_html_node(tn) for tn in textnodes]
                    li_node = ParentNode(tag="li", children=children)
                    li_nodes.append(li_node)
            node = ParentNode(tag="ol", children=li_nodes)
            new.append(node)
        elif block_type == BlockType.CODE:
            lines = block.split('\n')
            if lines[0].strip() == "```":
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines)
            code_node = LeafNode(tag="code", value=content)
            node = ParentNode(tag="pre", children=[code_node])
            new.append(node)
    parent = ParentNode(tag='div', children=new)
    return parent




