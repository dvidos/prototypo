from core.parser import parse_entities
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
    entities = parse_entities(text)
    for plugin in PLUGINS:
        for entity in entities:
            plugin.on_entity_declared(entity)
    sql = generate_sql(entities)
    return {'sql': sql}

