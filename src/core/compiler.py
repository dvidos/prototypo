from core.parser import parse_blocks
from core.codegen.sql import generate_sql
from core.plugin_manager import PluginManager

def compile_model(text):
    blocks = parse_blocks(text)
    context = {"errors": [], "output": []}

    manager = PluginManager()
    print("Loading plugins...")
    manager.load_plugins()
    print("Plugins found:")
    manager.list_plugins()
    print("Running actions:")
    manager.dispatch_blocks(blocks, context)
    manager.run_hook("on_validate", blocks, context)

    sql = generate_sql([b for b in blocks if b['type'] == 'entity'])
    return {'sql': sql, 'blocks': blocks, 'context': context}
