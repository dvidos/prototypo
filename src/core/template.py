import os
from jinja2 import Environment, FileSystemLoader

class TemplateRenderer:
    def __init__(self, base_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(base_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, template_path: str, context: dict) -> str:
        template = self.env.get_template(template_path)
        return template.render(context)
