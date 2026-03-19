import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestBlockSplit(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_not_two_lines(self):
        md = """
Block 1





Block 2
Still Block 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2\nStill Block 2"])


class TestBlockID(unittest.TestCase):
    def test_heading_three(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = """```
print(f)

```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = """> This
>is
> a
>quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = """- this
- is
- a
- list"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = """1. this
2. is
3. a
4. list"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_not_ordered_list_space(self):
        block = """1.this
2. is
3. a
4. list"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_ordered_list_numbers(self):
        block = """1. this
1. is
3. a
4. list"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_not_unordered_list_space(self):
        block = """- this
-is
- a
- list"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
