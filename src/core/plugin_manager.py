from typing import List
import importlib
import inspect
import os
from core.compiler_phase import CompilerPhase
from core.plugin_registration import PluginRegistration, SystemHook, BlockHook
from core.run_context import RunContext
from importlib import util


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
                if registration is not None:
                    self.registrations.append(registration)

    def run_system_hook(self, phase: CompilerPhase, blocks, context: RunContext):
        for reg in self.registrations:
            for hook in reg.system_hooks:
                if hook.phase != phase:
                    continue
                print("- " + str(hook.phase) + " on " + reg.name)
                hook.callback(blocks, context)

    def run_block_hook(self, phase: CompilerPhase, blocks, context: RunContext):
        for registration in self.registrations:
            for hook in registration.block_hooks:
                if hook.phase != phase:
                    continue
                for block in blocks:
                    self._run_block_hook_recursively(phase, registration, hook, block, context)

    def _run_block_hook_recursively(self, phase: CompilerPhase, registration: PluginRegistration, hook: BlockHook, block, context: RunContext):
        # call hook if block type matches
        call_needed = hook.block_type is None or hook.block_type == "*" or block.type == hook.block_type
        if call_needed:
            print("- " + str(hook.phase) + "(" + str(block.type) + " " + str(block.name) + ") on " + registration.name)
            hook.callback(block, context)

        # recurse
        for child in block.get_children():
            self._run_block_hook_recursively(phase, registration, hook, child, context)

    def list_plugins(self):
        for registration in self.registrations:
            print(" - " + registration.name)
