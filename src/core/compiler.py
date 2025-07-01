from core.parser import parse_blocks
from core.compiler_phase import CompilerPhase
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
        _run_phase(manager, CompilerPhase.SYS_INIT, True, blocks, context)
        _run_phase(manager, CompilerPhase.VALIDATE, False, blocks, context)
        _run_phase(manager, CompilerPhase.TRANSFORM, False, blocks, context)
        _run_phase(manager, CompilerPhase.GENERATE, False, blocks, context)
        _run_phase(manager, CompilerPhase.SYS_FINALIZE, True, blocks, context)
    except Exception as e:
        print("Errors! " + str(e))
        traceback.print_exc()
        return

    print("Success!")


def _run_phase(manager: PluginManager, phase: CompilerPhase, is_system: bool, blocks, context: RunContext):
    if is_system:
        manager.run_system_hook(phase, blocks, context)
    else:
        manager.run_block_hook(phase, blocks, context)

    if context.errors:
        raise RuntimeError("- " + "\n- ".join(context.errors))

