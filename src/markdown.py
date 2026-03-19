import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split = node.text.split(delimiter, maxsplit=2)
            if len(split) == 2:
                raise ValueError(f"{node.text} is missing closing {delimiter}.")
            elif len(split) == 1:
                new_nodes.append(node)
                continue
            split_nodes = [
                TextNode(split[0], TextType.TEXT),
                TextNode(split[1], text_type),
            ]
            if len(split[2]) > 0:
                # Recursively process any further pairs
                split_nodes.extend(
                    split_nodes_delimiter(
                        [TextNode(split[2], TextType.TEXT)], delimiter, text_type
                    )
                )
            new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def make_split_nodes_url(extract_func, text_type, prefix=""):
    def split_nodes_func(old_nodes):
        new_nodes = []
        for node in old_nodes:
            matches = extract_func(node.text)
            if len(matches) == 0:
                new_nodes.append(node)
            else:
                match_text = node.text
                for text, url in matches:
                    string = f"{prefix}[{text}]({url})"
                    begin, match_text = match_text.split(string, maxsplit=1)
                    if len(begin) > 0:
                        new_nodes.append(TextNode(begin, TextType.TEXT))
                    new_nodes.append(TextNode(text, text_type, url))
                if len(match_text) > 0:
                    new_nodes.append(TextNode(match_text, TextType.TEXT))
        return new_nodes

    return split_nodes_func


split_nodes_link = make_split_nodes_url(extract_markdown_links, TextType.LINK)
split_nodes_image = make_split_nodes_url(extract_markdown_images, TextType.IMAGE, "!")


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
