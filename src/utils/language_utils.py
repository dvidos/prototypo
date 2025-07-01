import re
import inflect

_inflector = inflect.engine()

def to_plural(word):
    return _inflector.plural(word)

def to_singular(word):
    return _inflector.singular_noun(word) or word

def to_snake_case(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def to_kebab_case(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()

def to_pascal_case(s):
    parts = re.split(r'[^a-zA-Z0-9]', s)
    return ''.join(word.capitalize() for word in parts if word)

def to_camel_case(s):
    pascal = to_pascal_case(s)
    return pascal[0].lower() + pascal[1:] if pascal else pascal

def to_screaming_snake_case(s):
    return to_snake_case(s).upper()
