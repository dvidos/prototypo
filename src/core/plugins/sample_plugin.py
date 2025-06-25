
class SamplePlugin:
    def register(self):
        return {
            "name": "Sample Plugin",
            "block_types": ['*'],
            "hooks": {
                "on_block": self.on_block_declared
            }
        }

    def on_block_declared(self, block):
        print(f"[SamplePlugin] Block declared: {block['name']}")
