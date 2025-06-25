from core.parser import parse_blocks
from core.codegen.sql import generate_sql
from core.plugin_manager import PluginManager, RunContext


def compile_model(text):
    blocks = parse_blocks(text)
    manager = PluginManager()

    print("Loading plugins...")
    manager.load_plugins()

    print("Plugins found:")
    manager.list_plugins()

    print("Running actions:")
    context = RunContext()
    manager.run_hook_with_args("on_init", blocks, context)
    manager.run_hook_per_block("validate", blocks, context)
    manager.run_hook_per_block("transform", blocks, context)
    manager.run_hook_per_block("generate", blocks, context)
    manager.run_hook_with_args("on_finalize", blocks, context)

    return {'status': 'done'}
