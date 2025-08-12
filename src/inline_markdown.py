from htmlnode import HTMLNode, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        image = extract_markdown_images(old_node.text)
        if image == []:
            new_nodes.append(old_node)
        else:
            curr_text = old_node.text
            for i in image:
                alt_url = i
                sections = curr_text.split(f"![{alt_url[0]}]({alt_url[1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_url[0], TextType.IMAGE, alt_url[1]))
                curr_text = sections[1]
            if curr_text:
                new_nodes.append(TextNode(curr_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        link = extract_markdown_links(old_node.text)
        if link == []:
            new_nodes.append(old_node)
        else:
            curr_text = old_node.text
            for i in link:
                link_text = i
                sections = curr_text.split(f"[{link_text[0]}]({link_text[1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text[0], TextType.LINK, link_text[1]))
                curr_text = sections[1]
            if curr_text:
                new_nodes.append(TextNode(curr_text, TextType.TEXT))
    return new_nodes