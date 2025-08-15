from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"

def block_to_block_type(block):
    items1 = block.split(" ")
    first_item = items1[0]
    items2 = block.split("\n")
    second_item = items2[0]


    if first_item.count("#") == len(first_item) and 1<= len(first_item) <= 6:
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif second_item.startswith(">"):
        is_quote = True
        for item in items2:
            if not item.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    elif second_item.startswith("- "):
        is_unordered = True
        for item in items2:
            if not item.startswith("- "):
                is_unordered = False
                break
        if is_unordered:
            return BlockType.UNORDERED
    elif second_item.startswith("1. "):
        is_ordered = True
        for i, item in enumerate(items2):
            if not item.startswith(f"{i+1}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH