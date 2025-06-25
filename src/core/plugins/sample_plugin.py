
class Plugin:
    def on_entity_declared(self, entity):
        print(f"[plugin] Entity declared: {entity['name']}")
