from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        start_index = text.find(delimiter)
        if start_index == -1:
            new_nodes.append(node)
            continue
        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            raise ValueError(f"No closing delimiter found for {delimiter}")
        
        before_text = text[:start_index]
        if before_text:
            new_nodes.append(TextNode(before_text, TextType.TEXT))
        
        middle_text = text[start_index + len(delimiter):end_index]
        new_nodes.append(TextNode(middle_text, text_type))
        
        after_text = text[end_index + len(delimiter):]
        if after_text:
            new_nodes.append(TextNode(after_text, TextType.TEXT))
        
    return new_nodes