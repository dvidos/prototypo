
class SamplePlugin:
    def on_block_declared(self, block):
        print(f"[SamplePlugin] Block declared: {block['name']}")
