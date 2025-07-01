from typing import List
import importlib
import inspect
import os
from core.run_context import RunContext
from importlib import util


class PluginRegistration:
    def __init__(self, name, block_types=None, hooks=None):
        self.name = name
        self.block_types = block_types or []
        self.hooks = hooks or {}

class PluginManager:
    def __init__(self):
        self.registrations: List[PluginRegistration] = []

    def load_plugins(self, plugin_package_path="core.plugins"):
        plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')

        for entry in sorted(os.listdir(plugin_dir)):
            entry_path = os.path.join(plugin_dir, entry)

            # Case 1: Subdirectory containing plugin.py
            if os.path.isdir(entry_path):
                plugin_file = os.path.join(entry_path, "plugin.py")
                if os.path.isfile(plugin_file):
                    spec = importlib.util.spec_from_file_location(f"{plugin_package_path}.{entry}.plugin", plugin_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self._register_plugin_classes(module)
                    continue

            # Case 2: Flat module-style plugin (e.g. sql_generator.py)
            if os.path.isfile(entry_path) and entry.endswith(".py") and entry != "__init__.py":
                full_module_name = f"{plugin_package_path}.{entry[:-3]}"
                module = importlib.import_module(full_module_name)
                self._register_plugin_classes(module)

    def _register_plugin_classes(self, module):
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.endswith("Plugin"):
                instance = obj()
                registration = instance.register()
                self.registrations.append(registration)

    def run_hook_with_args(self, hook_name, blocks, context: RunContext):
        for reg in self.registrations:
            if hook_name in reg.hooks:
                reg.hooks[hook_name](blocks, context)

    def run_hook_per_block(self, hook_name, blocks, context: RunContext):
        for reg in self.registrations:
            if hook_name not in reg.hooks:
                continue
            callback = reg.hooks[hook_name]
            for block in blocks:
                self._run_block_hook_recursively(callback, block, reg.block_types, context)

    def _run_block_hook_recursively(self, callback, block, block_types: List, context: RunContext):
        if block_types and block.type not in block_types:
            return
        callback(block, context)
        for child in block.children:
            self._run_block_hook_recursively(callback, child, block_types, context)

    def list_plugins(self):
        for registration in self.registrations:
            print(" - " + registration.name)
