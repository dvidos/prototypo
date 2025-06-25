import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


def tokenize(text):
    keywords = {'entity', 'fields'}
    token_spec = [
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('NAME', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SKIP', r'[ \t\n]+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        if kind == 'NAME' and value in keywords:
            kind = 'KEYWORD'
        yield Token(kind, value)


def parse_entities(text):
    tokens = list(tokenize(text))
    pos = 0

    def expect(type_):
        nonlocal pos
        if pos >= len(tokens) or tokens[pos].type != type_:
            raise SyntaxError(f"Expected {type_} at position {pos}, got {tokens[pos]}")
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_entity():
        expect('KEYWORD')  # 'entity'
        name = expect('NAME').value
        expect('LBRACE')
        expect('KEYWORD')  # 'fields'
        expect('LBRACE')
        fields = []
        while tokens[pos].type == 'NAME':
            fields.append(expect('NAME').value)
        expect('RBRACE')
        expect('RBRACE')
        return {'name': name, 'fields': fields}

    entities = []
    while pos < len(tokens):
        entities.append(parse_entity())
    return entities

