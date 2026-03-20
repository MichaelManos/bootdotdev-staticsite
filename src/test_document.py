import unittest

from htmlnode import ParentNode, LeafNode
from document import (
    make_heading,
    make_code,
    make_quote,
    make_ul,
    make_ol,
    make_paragraph,
    markdown_to_html_node,
)


class test_make_heading(unittest.TestCase):
    def test_heading_three(self):
        block = "### Heading _3_"
        expected = ParentNode("h3", [LeafNode(None, "Heading "), LeafNode("i", "3")])
        self.assertEqual(make_heading(block), expected)

    def test_code(self):
        block = """```
print(f)
```"""
        expected = ParentNode(
            "pre", [ParentNode("code", [LeafNode(None, "print(f)\n")])]
        )
        self.assertEqual(make_code(block), expected)

    def test_make_quote(self):
        block = """> This
> is
>**a**
>quote"""
        expected = ParentNode(
            "blockquote",
            [
                LeafNode(None, "This\nis\n"),
                LeafNode("b", "a"),
                LeafNode(None, "\nquote"),
            ],
        )
        self.assertEqual(make_quote(block), expected)

    def test_ul(self):
        block = """- item1
- item2"""
        expected = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "item1")]),
                ParentNode("li", [LeafNode(None, "item2")]),
            ],
        )
        self.assertEqual(make_ul(block), expected)

    def test_ol(self):
        block = """1. item1
2. item2"""
        expected = ParentNode(
            "ol",
            [
                ParentNode("li", [LeafNode(None, "item1")]),
                ParentNode("li", [LeafNode(None, "item2")]),
            ],
        )
        self.assertEqual(make_ol(block), expected)

    def test_paragraph(self):
        block = """This
is a _paragraph_
of text"""
        expected = ParentNode(
            "p",
            [
                LeafNode(None, "This is a "),
                LeafNode("i", "paragraph"),
                LeafNode(None, " of text"),
            ],
        )
        self.assertEqual(make_paragraph(block), expected)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
