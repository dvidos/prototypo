from core.parser import parse_blocks
from core.plugin_manager import PluginManager
from core.run_context import RunContext


def compile_model(text):
    blocks = parse_blocks(text)
    manager = PluginManager()

    print("Loading plugins...")
    manager.load_plugins()

    print("Plugins found:")
    manager.list_plugins()

    print("Running actions:")
    context = RunContext("./out/")
    manager.run_hook_with_args("on_init", blocks, context)
    manager.run_hook_per_block("validate", blocks, context)
    manager.run_hook_per_block("transform", blocks, context)
    manager.run_hook_per_block("generate", blocks, context)
    manager.run_hook_with_args("on_finalize", blocks, context)

    return {'status': 'done'}
