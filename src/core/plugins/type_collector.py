from core.compiler_phase import CompilerPhase
from core.model.backend.value_type import ValueType
from core.model.block import Block
from core.plugin_registration import PluginRegistration, BlockHook
from core.run_context import RunContext


class TypeCollectorPlugin:
    # This plugin is responsible for scaffolding backend controllers, frontend screens, and relational schemas

    def register(self):
        return PluginRegistration(
            name="Type Collector",
            block_hooks=[
                BlockHook(CompilerPhase.TYPE_COLLECTION, "type", self.on_type_collection),
                BlockHook(CompilerPhase.VALIDATE, "type", self.on_type_validation),
            ]
        )

    def on_type_collection(self, block: Block, context: RunContext):
        if block.type != "type":
            return

        if context.backend_app.has_type(block.name):
            context.error(f"Type '{block.name}' is already defined")
            return

        context.backend_app.register_type(ValueType(
            name=block.name,
            description=block.get_assignment_value("description", ""),
            base_type=block.get_assignment_value("base_type", "String")
        ))


    def on_type_validation(self, block: Block, context: RunContext):
        if block.type != "type":
            return

        if not context.backend_app.has_type(block.name):
            context.error(f"Type '{block.name}' is not defined")
            return

        type = context.backend_app.get_type(block.name)
        if context.backend_app.has_type(type.base_type):
            context.error(f"Base type '{type.base_type}' is not defined for type '{type.name}'")
