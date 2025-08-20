def markdown_to_blocks(md):
    finished_blocks = []
    blocks = md.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block:
            finished_blocks.append(block)
    return finished_blocks



