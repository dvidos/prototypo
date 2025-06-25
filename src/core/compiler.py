from core.parser import parse_blocks
from core.codegen.sql import generate_sql
import importlib
import os
import pkgutil

PLUGINS = []

def load_plugins():
    global PLUGINS
    plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    for finder, name, ispkg in pkgutil.iter_modules([plugin_dir]):
        full_name = f"core.plugins.{name}"
        module = importlib.import_module(full_name)
        if hasattr(module, 'Plugin'):
            PLUGINS.append(module.Plugin())

def compile_model(text):
    load_plugins()
    blocks = parse_blocks(text)
    for plugin in PLUGINS:
        for block in blocks:
            plugin.on_block_declared(block)
    sql = generate_sql(blocks)
    return {'sql': sql}

