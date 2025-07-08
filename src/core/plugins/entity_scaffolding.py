from typing import Optional

from core.model.backend.service import Service, Action
from core.model.block import Block
from core.model.backend.controller import Controller
from core.model.backend.data_model import DataModel
from core.model.backend.endpoint import Endpoint
from core.model.backend.entity import Entity, Attribute
from core.model.relational_schema.column import DataType, Column
from core.model.relational_schema.sql_table import SqlTable
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
        entity = self._create_backend_entity(block, context)
        if not entity:
            return
        context.backend_app.add_entity(entity)

        self.populate_frontend_screen(block, context)


    def _create_backend_entity(self, block: Block, context: RunContext) -> Optional[Entity]:
        # here we define the DDD entity, as well as the relational schema table
        # so, the storage strategy is defined here
        attributes_block = block.get_child("attributes")
        if not attributes_block:
            context.error(f"Entity block '{block.name}' must have an 'attributes' child block with attributes defined.")
            return None

        identity = self._derive_identity_attribute_from_block(attributes_block, context)
        if identity is None:
            return None

        entity = Entity(block.name, identity)
        self._derive_other_attributes_from_block(attributes_block, entity, context)

        table = self._derive_related_sql_table(entity, context)

        context.sql_schema.add_table(table)
        entity.related_controller = self._create_backend_controller(block, context)
        entity.related_service = self._create_backend_service(block, context)

        return entity


    def _derive_identity_attribute_from_block(self, attributes_block: Block, context: RunContext) -> Optional[Attribute]:
        identity = None

        if attributes_block.has_assignment("id"):
            # if there is an assignment with "id", we assume it is the primary key
            assignment = attributes_block.get_assignment("id")
            type = assignment.type if assignment.type else "integer"
            identity = Attribute(name="id", type=type)

        if identity is None and attributes_block.has_child("id"):
            # if there is a child block with name = "id", we assume it is the primary key
            id_block = attributes_block.get_child("id")
            type = id_block.get_assignment("type").value if id_block.has_assignment("type") else "integer"
            identity = Attribute(name="id", type=type)

        if identity is None:
            # look for a subblock with "primary_key" assignment
            for child in attributes_block.get_children():
                if not child.has_assignment("primary_key"):
                    continue
                name = child.name if child.name else \
                       child.get_assignment("name").value if child.has_assignment("name") else \
                       "id"
                type = child.get_assignment("type").value if child.has_assignment("type") else "integer"
                identity = Attribute(name=name, type=type)
                break

        if identity is None:
            # if no id attribute is defined, we create a default one
            identity = Attribute(name="id", type="integer")

        return identity

    def _derive_other_attributes_from_block(self, attributes_block: Block, entity: Entity, context: RunContext):
        # go over all assignments and children in the attributes block
        for assignment in attributes_block._assignments:
            name = assignment.name
            if name == entity.id.name:  # skip the primary key
                continue
            type = assignment.type if assignment.type else "string"
            entity.add_attribute(Attribute(name=name, type=type))

        for child in attributes_block.get_children():
            # either use the name of the block or the assignment "name" if it exists
            name = child.name if child.name else \
                   child.get_assignment("name").value if child.has_assignment("name") else \
                   None
            if not name:
                context.error(f"Child blocks in attributes must have a name or 'name' assignment.")
                continue
            if name == entity.id.name:  # skip the primary key
                continue

            type = child.get_assignment("type").value if child.has_assignment("type") else "string"
            entity.add_attribute(Attribute(name=name, type=type))
            # we could also derive relationships here, but for now we just focus on attributes
            # for example a list of OrderLines for an Order entity could be derived here

    def _derive_related_sql_table(self, entity: Entity, context: RunContext) -> SqlTable:
        table = SqlTable(name=to_snake_case(to_plural(entity.name)))

        # first, we add the primary key column
        column = self._derive_relational_schema_column(entity, entity.id, context)
        entity.id.related_sql_column = column
        table.add_column(column)

        for attribute in entity.attributes:
            column = self._derive_relational_schema_column(entity, attribute, context)
            attribute.related_sql_column = column
            table.add_column(column)

        entity.related_sql_table = table
        return table

    def _derive_relational_schema_column(self, entity: Entity, attribute: Attribute, context: RunContext) -> Column:
        # this method derives a relational schema column from an attribute
        name = to_snake_case(attribute.name)
        type = self._derive_data_type_from_attribute_type(attribute.type)
        primary_key = (attribute.name == entity.id.name)  # if this is the id attribute, it is a primary key
        auto_increment = (attribute.type == "integer" and primary_key)  # only integer id attributes can be auto-incremented
        return Column(name=name, type=type, primary_key=primary_key, auto_increment=auto_increment)

    def _derive_data_type_from_attribute_type(self, attribute_type: str) -> DataType:
        return DataType.INT if attribute_type == "integer" else \
               DataType.FLOAT if attribute_type == "float" else \
               DataType.BOOLEAN if attribute_type == "boolean" else \
               DataType.DATE if attribute_type == "date" else \
               DataType.TIMESTAMP if attribute_type == "datetime" else \
               DataType.STRING  # default to STRING if no match found


    def _create_backend_controller(self, block: Block, context: RunContext):

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
        return controller


    def _create_backend_service(self, block: Block, context: RunContext):
        service = Service(to_plural(to_pascal_case(block.name)))

        actions_block = block.get_child("actions")
        if actions_block is not None:

            for child in actions_block.get_children():
                action = Action(
                    name=child.name,
                    description=child.get_assignment_value("description", None),
                )
                service.add_action(action)

            for assignment in actions_block._assignments:
                action = Action(
                    name=assignment.name,
                    description=assignment.value
                )
                service.actions.append(action)

        return service


    def populate_frontend_screen(self, block: Block, context: RunContext):
        # this is a placeholder for future frontend screen generation
        # currently, we do not generate any frontend screens from the entity block
        # but we could add logic here to create React components, pages, etc.
        pass

