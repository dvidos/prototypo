import importlib
import inspect
import os
import pkgutil

class PluginManager:
    def __init__(self):
        self.plugins = []
        self.hooks = {
            "on_block": [],
            "on_validate": [],
            "on_transform": [],
            "on_generate_sql": [],
            "on_finalize": []
        }
        self.block_type_map = {}

    def load_plugins(self, plugin_package_path="core.plugins"):
        plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        for _, module_name, _ in pkgutil.iter_modules([plugin_dir]):
            print("** " + module_name)
            full_module_name = f"{plugin_package_path}.{module_name}"
            module = importlib.import_module(full_module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith("Plugin"):
                    print("** instantiating " + str(name) + " " + str(obj))
                    instance = obj()
                    registration = instance.register()

                    self.plugins.append(registration)

                    for hook_name, callback in registration.get("hooks", {}).items():
                        self.hooks.setdefault(hook_name, []).append(callback)

                    for btype in registration.get("block_types", []):
                        self.block_type_map.setdefault(btype, []).append(instance)

    def run_hook(self, hook_name, *args):
        for fn in self.hooks.get(hook_name, []):
            fn(*args)

    def dispatch_blocks(self, blocks, context):
        for block in blocks:
            for plugin in self.block_type_map.get(block['type'], []):
                cb = plugin.register().get('hooks', {}).get('on_block')
                if cb:
                    cb(block, context)

    def list_plugins(self):
        return [plugin.get("name", "Unnamed Plugin") for plugin in self.plugins]


