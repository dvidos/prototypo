from core.plugin_manager import PluginRegistration, RunContext

class SamplePlugin:
    def register(self):
        return PluginRegistration(
            name="Sample Plugin",
            block_types=[],
            hooks={
                "on_init": self.on_init,
                "validate": self.validate,
                "transform": self.transform,
                "generate": self.generate,
                "on_finalize": self.on_finalize
            }
        )

    def on_block_declared(self, block):
        print(f"[SamplePlugin] Block declared: {block['name']}")

    def on_init(self, blocks, context: RunContext):
        print("[SamplePlugin] on_init()")

    def validate(self, block, context: RunContext):
        print("[SamplePlugin] validate(), block=" + block['name'])

    def transform(self, block, context: RunContext):
        print("[SamplePlugin] transform(), block=" + block['name'])

    def generate(self, block, context: RunContext):
        print("[SamplePlugin] generate(), block=" + block['name'])

    def on_finalize(self, blocks, context: RunContext):
        print("[SamplePlugin] on_finalize()")
