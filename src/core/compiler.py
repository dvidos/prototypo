from core.parser import parse_blocks
from core.plugin_manager import PluginManager
from core.run_context import RunContext
import traceback


def compile_model(text):
    blocks = parse_blocks(text)
    manager = PluginManager()

    print("Loading plugins...")
    manager.load_plugins()

    print("Plugins found:")
    manager.list_plugins()

    print("Running actions:")
    context = RunContext("./out/")

    try:
        run_phase(manager, 'on_init', False, blocks, context)
        run_phase(manager, 'validate', True, blocks, context)
        run_phase(manager, 'transform', True, blocks, context)
        run_phase(manager, 'generate', True, blocks, context)
        run_phase(manager, 'on_finalize', False, blocks, context)
    except Exception as e:
        print("Errors! " + str(e))
        traceback.print_exc()
        return

    print("Success!")


def run_phase(manager: PluginManager, hook_name: str, per_block: bool, blocks, context: RunContext):
    if per_block:
        manager.run_hook_per_block(hook_name, blocks, context)
    else:
        manager.run_hook_with_args(hook_name, blocks, context)
    if context.errors:
        raise RuntimeError("- " + "\n- ".join(context.errors))

