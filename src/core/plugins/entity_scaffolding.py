from core.model.backend.endpoint import Endpoint
from core.plugin_manager import PluginRegistration
from core.run_context import RunContext
from utils.language_utils import to_plural, to_singular, to_pascal_case


class EntityScaffoldingPlugin:
    def register(self):
        return PluginRegistration(
            name="Entity Scaffolding Plugin",
            block_types=['entity'],
            hooks={
                "on_init": self.on_init,
                "validate": self.validate,
                "transform": self.transform,
                "generate": self.generate,
                "on_finalize": self.on_finalize
            }
        )

    def on_init(self, blocks, context: RunContext):
        # we could validate if we have any entities first
        ...

    def validate(self, block, context: RunContext):
        ...

    def transform(self, block, context: RunContext):
        ...

    def generate(self, block, context: RunContext):
        if block.type != "entity":
            return
        # generate base CRUD endpoints for the entity
        context.backend_app.add_endpoint(Endpoint(
            path="/" +  to_plural(block.name.lower()),
            method="GET",
            handler_name=f"get_{to_plural(block.name.lower())}",
            name="List " + to_plural(block.name),
            summary=f"Get all {to_plural(block.name)}",
        ))
        context.backend_app.add_endpoint(Endpoint(
            path="/" +  to_plural(block.name.lower()) + "/{id}",
            identifier_name="id",
            method="GET",
            handler_name=f"get_{to_singular(block.name.lower())}",
            response_model=to_pascal_case(block.name) + "Response",
            name="Read " + to_singular(block.name),
            summary=f"Get one {to_singular(block.name)}",
        ))
        context.backend_app.add_endpoint(Endpoint(
            path="/" +  to_plural(block.name.lower()),
            method="POST",
            handler_name=f"create_{to_singular(block.name.lower())}",
            request_model=to_pascal_case(block.name) + "CreateRequest",
            response_model=to_pascal_case(block.name) + "Response",
            name="Create " + to_singular(block.name),
            summary=f"Create a new {to_singular(block.name)}",
        ))
        context.backend_app.add_endpoint(Endpoint(
            path="/" +  to_plural(block.name.lower()) + "/{id}",
            identifier_name="id",
            method="PUT",
            handler_name=f"update_{to_singular(block.name.lower())}",
            request_model=to_pascal_case(block.name) + "UpdateRequest",
            response_model=to_pascal_case(block.name) + "Response",
            name="Update " + to_singular(block.name),
            summary=f"Update an existing {to_singular(block.name)}",
        ))
        context.backend_app.add_endpoint(Endpoint(
            path="/" +  to_plural(block.name.lower()) + "/{id}",
            identifier_name="id",
            method="DELETE",
            handler_name=f"delete_{to_singular(block.name.lower())}",
            name="Delete " + to_singular(block.name),
            summary=f"Delete an existing {to_singular(block.name)}",
        ))
        # then we could generate one endpoint for each action (subscribe, unsubscribe, etc.)

    def on_finalize(self, blocks, context: RunContext):
        ...

