import re

# Constants
T_LBRACE = '{'
T_RBRACE = '}'
COMMENT_CHAR = '#'

def strip_inline_comment(line):
    return line.split(COMMENT_CHAR, 1)[0].rstrip()

def parse_assignment_line(line):
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

    return {'type': a_type, 'name': a_name, 'value': value}

def parse_block_lines(lines, start_index=0):
    assignments = []
    children = []
    i = start_index

    while i < len(lines):
        line = strip_inline_comment(lines[i]).strip()
        if not line:
            i += 1
            continue

        if line == T_RBRACE:
            return {'assignments': assignments, 'children': children}, i + 1

        if line.endswith(T_LBRACE):
            prefix = line[:-1].strip()
            parts = prefix.split(None, 1)
            if len(parts) == 2:
                block_type, block_name = parts
            else:
                block_type, block_name = None, parts[0]

            nested_block, next_i = parse_block_lines(lines, i + 1)
            nested_block.update({'type': block_type, 'name': block_name})
            children.append(nested_block)
            i = next_i
        else:
            assignment = parse_assignment_line(line)
            if assignment:
                assignments.append(assignment)
            i += 1

    raise SyntaxError("Expected '}' but reached end of input")

def parse_blocks(text):
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
            block, next_i = parse_block_lines(lines, i + 1)
            block.update({'type': None, 'name': None})
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

            block, next_i = parse_block_lines(lines, i + 1)
            block.update({'type': block_type, 'name': block_name})
            blocks.append(block)
            i = next_i
            continue

        raise SyntaxError(f"Unexpected line outside block at {i+1}: {lines[i]}")

    return blocks
