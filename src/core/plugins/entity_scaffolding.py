from core.model.backend.controller import Controller
from core.model.backend.data_model import DataModel
from core.model.backend.endpoint import Endpoint
from core.plugin_registration import PluginRegistration, BlockHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from utils.language_utils import to_plural, to_singular, to_pascal_case


class EntityScaffoldingPlugin:
    def register(self):
        return PluginRegistration(
            name="Entity Scaffolding Plugin",
            block_hooks=[
                BlockHook(CompilerPhase.POPULATE, "entity", self.populate),
            ]
        )

    def populate(self, block, context: RunContext):
        if block.type != "entity":
            return

        controller = Controller(to_plural(to_pascal_case(block.name)))

        controller.models.append(DataModel(to_pascal_case(block.name) + "Response", {"attr1": "str"}))
        controller.models.append(DataModel(to_pascal_case(block.name) + "CreateRequest", {"attr1": "str"}))
        controller.models.append(DataModel(to_pascal_case(block.name) + "UpdateRequest", {"attr1": "str"}))

        identifier_name = to_singular(block.name.lower()) + "_id"

        # generate base CRUD endpoints for the entity
        controller.endpoints.append(Endpoint(
            path="/",
            method="GET",
            handler_name=f"get_{to_plural(block.name.lower())}",
            name="List " + to_plural(block.name),
            summary=f"Get all {to_plural(block.name)}, requires pagination, filtering, sorting, etc.",
        ))
        controller.endpoints.append(Endpoint(
            path="/{id}",
            identifier_name=identifier_name,
            method="GET",
            handler_name=f"get_{to_singular(block.name.lower())}",
            response_model=to_pascal_case(block.name) + "Response",
            name="Read " + to_singular(block.name),
            summary=f"Get one {to_singular(block.name)}",
        ))
        controller.endpoints.append(Endpoint(
            path="/",
            method="POST",
            handler_name=f"create_{to_singular(block.name.lower())}",
            request_model=to_pascal_case(block.name) + "CreateRequest",
            response_model=to_pascal_case(block.name) + "Response",
            name="Create " + to_singular(block.name),
            summary=f"Create a new {to_singular(block.name)}",
        ))
        controller.endpoints.append(Endpoint(
            path="/{id}",
            identifier_name=identifier_name,
            method="PUT",
            handler_name=f"update_{to_singular(block.name.lower())}",
            request_model=to_pascal_case(block.name) + "UpdateRequest",
            response_model=to_pascal_case(block.name) + "Response",
            name="Update " + to_singular(block.name),
            summary=f"Update an existing {to_singular(block.name)}",
        ))
        controller.endpoints.append(Endpoint(
            path="/{id}",
            identifier_name=identifier_name,
            method="DELETE",
            handler_name=f"delete_{to_singular(block.name.lower())}",
            name="Delete " + to_singular(block.name),
            summary=f"Delete an existing {to_singular(block.name)}",
        ))
        # then we could generate one endpoint for each action (subscribe, unsubscribe, etc.)
        context.backend_app.add_controller(controller)


