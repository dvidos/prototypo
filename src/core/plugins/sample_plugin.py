from core.compiler_phase import CompilerPhase
from core.plugin_registration import PluginRegistration, SystemHook, BlockHook
from core.run_context import RunContext


class SamplePlugin:
    def register(self):
        return PluginRegistration(name="Sample Plugin",
            system_hooks=[
                SystemHook(CompilerPhase.SYS_INIT, self.on_init),
                SystemHook(CompilerPhase.SYS_GENERATE_OUT, self.on_generate),
                SystemHook(CompilerPhase.SYS_FINALIZE, self.on_finalize)
            ],
            block_hooks=[
                BlockHook(CompilerPhase.VALIDATE, "*", self.validate),
                BlockHook(CompilerPhase.TRANSFORM, "*", self.transform),
                BlockHook(CompilerPhase.POPULATE, "*", self.populate),
            ]
        )

    def on_block_declared(self, block):
        # print(f"[SamplePlugin] Block declared: {block['name']}")
        ...

    def on_init(self, blocks, context: RunContext):
        # print("[SamplePlugin] on_init()")
        ...

    def validate(self, block, context: RunContext):
        # print("[SamplePlugin] validate(), block=" + block['name'])
        ...

    def transform(self, block, context: RunContext):
        # print("[SamplePlugin] transform(), block=" + block['name'])
        ...

    def populate(self, block, context: RunContext):
        # print("[SamplePlugin] populate(), block=" + block['name'])
        ...

    def on_generate(self, blocks, context: RunContext):
        # print("[SamplePlugin] on_generate()")
        ...

    def on_finalize(self, blocks, context: RunContext):
        # print("[SamplePlugin] on_finalize()")
        ...
