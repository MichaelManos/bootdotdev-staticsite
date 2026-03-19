import enum
import re


class BlockType(enum.Enum):
    PARAGRAPH = "BlockType.PARAGRAPH"
    HEADING = "BlockType.HEADING"
    CODE = "BlockType.CODE"
    QUOTE = "BlockType.QUOTE"
    UNORDERED_LIST = "BlockType.UNORDERED_LIST"
    ORDERED_LIST = "BlockType.ORDERED_LIST"


def markdown_to_blocks(markdown: str):
    return [block.strip() for block in markdown.split("\n\n") if len(block.strip()) > 0]


def block_to_block_type(block: str):
    if block.startswith("#"):
        return BlockType.HEADING
    if re.search(r"^```[\n\r]+[\s\S]*```$", block):
        return BlockType.CODE
    # Multi-line checks
    lines = block.split("\n")
    if len(lines) == len(list(filter(lambda x: x.startswith(">"), lines))):
        return BlockType.QUOTE
    if len(lines) == len(list(filter(lambda x: x.startswith("- "), lines))):
        return BlockType.UNORDERED_LIST
    # Line by line check:
    is_ordered_list = True
    for n, line in enumerate(lines):
        if not line.startswith(f"{n+1}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
