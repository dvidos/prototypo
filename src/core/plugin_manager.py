from typing import List
import importlib
import inspect
import os
import pkgutil

class PluginRegistration:
    def __init__(self, name, block_types=None, hooks=None):
        self.name = name
        self.block_types = block_types or []
        self.hooks = hooks or {}

class RunContext:
    def __init__(self):
        self.errors = []
        self.output = []

    def error(self, message):
        self.errors.append(message)

    def print(self, message):
        self.output.append(message)


class PluginManager:
    def __init__(self):
        self.registrations = []

    def load_plugins(self, plugin_package_path="core.plugins"):
        plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        for _, module_name, _ in pkgutil.iter_modules([plugin_dir]):
            full_module_name = f"{plugin_package_path}.{module_name}"
            module = importlib.import_module(full_module_name)

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
        if len(block_types) > 0 and block['type'] not in block_types:
            return
        callback(block, context)
        for child in block['children']:
            self._run_block_hook_recursively(callback, child, block_types, context)

    def list_plugins(self):
        for registration in self.registrations:
            print(" - " + registration.name)

