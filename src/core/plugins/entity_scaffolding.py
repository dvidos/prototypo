from core.model.block import Block
from core.model.backend.controller import Controller
from core.model.backend.data_model import DataModel
from core.model.backend.endpoint import Endpoint
from core.model.relational_schema.column import DataType, Column
from core.model.relational_schema.table import Table
from core.plugin_registration import PluginRegistration, BlockHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from utils.language_utils import to_plural, to_singular, to_pascal_case, to_snake_case


class EntityScaffoldingPlugin:
    # This plugin is responsible for scaffolding backend controllers, frontend screens, and relational schemas

    def register(self):
        return PluginRegistration(
            name="Entity Scaffolding Plugin",
            block_hooks=[
                BlockHook(CompilerPhase.POPULATE, "entity", self.populate),
            ]
        )

    def populate(self, block: Block, context: RunContext):
        if block.type != "entity":
            return
        self.populate_backend_controller(block, context)
        self.populate_frontend_screen(block, context)
        self.populate_relational_schema(block, context)

    def populate_backend_controller(self, block: Block, context: RunContext):

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


    def populate_frontend_screen(self, block: Block, context: RunContext):
        # this is a placeholder for future frontend screen generation
        # currently, we do not generate any frontend screens from the entity block
        # but we could add logic here to create React components, pages, etc.
        pass


    def populate_relational_schema(self, block: Block, context: RunContext):
        table = Table(name=to_snake_case(to_plural(block.name)))
        schema_types = {
            "string": DataType.STRING,
            "integer": DataType.INT,
            "float": DataType.FLOAT,
            "boolean": DataType.BOOLEAN,
            "date": DataType.DATE,
            "datetime": DataType.TIMESTAMP,
        }
        has_id_column = (block.has_child("attributes") and
                         (block.get_child("attributes").has_assignment("id")) or block.get_child("attributes").has_child("id"))

        if not has_id_column:
            # if there is no id column, we should add it as a primary key
            table.add_column(Column(
                name="id",
                type=DataType.INT,
                primary_key=True,
                auto_increment=True
            ))

        # all attributes are in the "attributes" child block, either as assignments or as child blocks
        if block.has_child("attributes"):
            entity_attributes = block.get_child("attributes")

            for a in entity_attributes.assignments:
                col_type = schema_types[a.type] if a.type in schema_types else DataType.STRING
                table.add_column(Column(
                    name=to_snake_case(a.name),
                    type=col_type
                ))

            for c in entity_attributes.children:
                if not c.has_assignment("name"):
                    context.error(f"Attribute block {c.name} must have a 'name' assignment")
                    continue
                c_name = c.get_assignment("name").value
                c_type = c.get_assignment("type").value if c.has_assignment("type") else "string"
                col_type = schema_types[c_type] if c_type in schema_types else DataType.STRING
                table.add_column(Column(
                    name=to_snake_case(c_name),
                    type=col_type,
                ))

        context.db_schema.add_table(table)

