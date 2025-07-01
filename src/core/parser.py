import re
from typing import Optional
from core.model.block import Block, Assignment

# Constants
T_LBRACE = '{'
T_RBRACE = '}'
COMMENT_CHAR = '#'

def strip_inline_comment(line):
    return line.split(COMMENT_CHAR, 1)[0].rstrip()

def parse_assignment_line(line) -> Optional[Assignment]:
    """
    Parse a single assignment line:
    Possible formats:
    - type name = value
    - name = value
    - type name
    - name
    """
    line = line.strip()
    if not line:
        return None

    # Split on '=' first
    if '=' in line:
        left, value = line.split('=', 1)
        value = value.strip()
    else:
        left, value = line, None

    left_parts = left.strip().split(None, 1)  # split by whitespace max 2 parts
    if len(left_parts) == 2:
        a_type, a_name = left_parts
    else:
        a_type = None
        a_name = left_parts[0]

    return Assignment(type=a_type, name=a_name, value=value)


def parse_block_lines(block: Block, lines, start_index=0) -> int:
    i = start_index

    while i < len(lines):
        line = strip_inline_comment(lines[i]).strip()
        if not line:
            i += 1
            continue

        if line == T_RBRACE:
            return i + 1

        if line.endswith(T_LBRACE):
            prefix = line[:-1].strip()
            parts = prefix.split(None, 1)
            if len(parts) == 2:
                block_type, block_name = parts
            else:
                block_type, block_name = None, parts[0]

            nested_block = Block(name=block_name, type=block_type)
            next_i = parse_block_lines(nested_block, lines, i + 1)
            block.children.append(nested_block)
            i = next_i
        else:
            assignment = parse_assignment_line(line)
            if assignment:
                block.assignments.append(assignment)
            i += 1

    raise SyntaxError("Expected '}' but reached end of input")

def parse_blocks(text) -> list[Block]:
    """
    Parse top-level blocks from the whole text.
    Supports:
    - optional block type and/or name
    - anonymous blocks
    """
    lines = text.splitlines()
    i = 0
    blocks = []

    while i < len(lines):
        line = strip_inline_comment(lines[i]).strip()
        if not line:
            i += 1
            continue

        if line == T_LBRACE:
            # anonymous block at top level
            block = Block(name=None, type=None)
            next_i = parse_block_lines(block, lines, i + 1)
            blocks.append(block)
            i = next_i
            continue

        if line.endswith(T_LBRACE):
            prefix = line[:-1].strip()
            parts = prefix.split(None, 1)
            if len(parts) == 2:
                block_type, block_name = parts
            else:
                block_type, block_name = None, parts[0]

            block = Block(name=block_name, type=block_type)
            next_i = parse_block_lines(block, lines, i + 1)
            blocks.append(block)
            i = next_i
            continue

        if line.endswith(T_LBRACE + T_RBRACE):
            prefix = line[:-2].strip()
            parts = prefix.split(None, 1)
            if len(prefix) == 0:
                block_type, block_name = None, None
            elif len(parts) == 2:
                block_type, block_name = parts
            else:
                block_type, block_name = None, parts[0]

            block = Block(name=block_name, type=block_type)
            blocks.append(block)
            next_i = i + 1
            i = next_i
            continue

        raise SyntaxError(f"Unexpected line outside block at {i+1}: {lines[i]}")

    return blocks
