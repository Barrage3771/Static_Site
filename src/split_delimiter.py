from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Process this text node
        curr_text = old_node.text
        while True:
            start_index = curr_text.find(delimiter)
            if start_index == -1:
                # No more delimiters, add remaining text and break
                if curr_text:
                    new_nodes.append(TextNode(curr_text, TextType.TEXT))
                break

            end_index = curr_text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise ValueError(f"No closing delimiter found for {delimiter}")

            # Add text before delimiter
            before_text = curr_text[:start_index]
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            # Add delimited text with special type
            delimited_text = curr_text[start_index + len(delimiter):end_index]
            new_nodes.append(TextNode(delimited_text, text_type))

            # Update current text to what remains
            curr_text = curr_text[end_index + len(delimiter):]

    return new_nodes