import re

import htmlnode as hn
import markdown as md
import textnode as tn
import blocks as bl


def markdown_to_html_node(markdown: str):
    blockfuncs = {
        bl.BlockType.CODE: make_code,
        bl.BlockType.HEADING: make_heading,
        bl.BlockType.ORDERED_LIST: make_ol,
        bl.BlockType.PARAGRAPH: make_paragraph,
        bl.BlockType.QUOTE: make_quote,
        bl.BlockType.UNORDERED_LIST: make_ul,
    }
    blocks = bl.markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = bl.block_to_block_type(block)
        children.append(blockfuncs[block_type](block))
    return hn.ParentNode("div", children)


def text_to_children(text):
    textnodes = md.text_to_textnodes(text)
    return [tn.text_node_to_html_node(node) for node in textnodes]


def strip_newline(string):
    return " ".join(string.split("\n"))


def make_heading(block):
    num_pounds = 0
    for i in range(6):
        if block[i] == "#":
            num_pounds += 1
        else:
            break
    text = strip_newline(block[num_pounds:].strip())
    children = text_to_children(text)
    return hn.ParentNode(tag=f"h{num_pounds}", children=children)


def make_code(block):
    text = re.match(r"^```[\n\r]+([\s\S]*)```$", block).group(1)
    child = tn.text_node_to_html_node(tn.TextNode(text, tn.TextType.TEXT))
    inner = hn.ParentNode("code", [child])
    return hn.ParentNode("pre", [inner])


def make_quote(block):
    lines = block.split("\n")
    stripped = [line[1:].lstrip() for line in lines]
    children = text_to_children("\n".join(stripped))
    return hn.ParentNode("blockquote", children)


def make_ul(block):
    lines = block.split("\n")
    stripped = [line[2:] for line in lines]
    return hn.ParentNode(
        "ul", [hn.ParentNode("li", text_to_children(line)) for line in stripped]
    )


def make_ol(block):
    lines = block.split("\n")
    newlines = []
    for n, line in enumerate(lines):
        newlines.append(line.replace(f"{n + 1}. ", ""))
    return hn.ParentNode(
        "ol", [hn.ParentNode("li", text_to_children(line)) for line in newlines]
    )


def make_paragraph(block):
    return hn.ParentNode("p", text_to_children(strip_newline(block)))
