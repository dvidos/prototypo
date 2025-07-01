from jinja2 import Environment, FileSystemLoader
from utils.language_utils import (
    to_plural,
    to_singular,
    to_snake_case,
    to_kebab_case,
    to_pascal_case,
    to_camel_case,
    to_screaming_snake_case,
)

class TemplateRenderer:
    def __init__(self, base_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(base_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Register filters
        self.env.filters['plural'] = to_plural
        self.env.filters['singular'] = to_singular
        self.env.filters['snake_case'] = to_snake_case
        self.env.filters['kebab_case'] = to_kebab_case
        self.env.filters['pascal_case'] = to_pascal_case
        self.env.filters['camel_case'] = to_camel_case
        self.env.filters['screaming_snake_case'] = to_screaming_snake_case

        # Use as thus:
        # {{"user" | plural}}                        → users
        # {{"categories" | singular}}                → category
        # {{"fish" | plural}}                        → fish
        # {{"CustomerService" | snake_case}}         → customer_service
        # {{"UserEmail" | kebab_case}}               → user-email
        # {{"some_value_here" | pascal_case}}        → SomeValueHere
        # {{"SomeValueHere" | camel_case}}           → someValueHere
        # {{"someValueHere" | screaming_snake_case}} → SOME_VALUE_HERE


    def render(self, template_path: str, context: dict) -> str:
        template = self.env.get_template(template_path)
        return template.render(context)
