import os

from core.model.backend.controller import Controller
from core.model.backend.entity import Entity
from core.template import TemplateRenderer
from core.plugin_registration import PluginRegistration, SystemHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from core.model.service_definition import ServiceDefinition
from utils.language_utils import to_snake_case


class BackendGeneratorPlugin:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self._renderer = TemplateRenderer(template_dir)

    def register(self):
        return PluginRegistration(
            name="Backend App Generator",
            system_hooks=[
                SystemHook(CompilerPhase.SYS_INIT, self.on_init),
                SystemHook(CompilerPhase.SYS_GENERATE_OUT, self.on_generate),
            ]
        )

    def on_init(self, blocks, context: RunContext):
        # we could validate if we have any entities first
        context.add_containerized_service(ServiceDefinition(
            name="backend",
            build_path="services/backend",
            dockerfile="Dockerfile",
            ports=["8080:8080"],
            depends_on=["db"]
        ))

    def on_generate(self, blocks, context: RunContext):
        self.generate_app_py(context)
        self.generate_modules(context)
        self.generate_requirements_txt(context)
        self.generate_dockerfile(context)

    def generate_app_py(self, context: RunContext):
        db_url = self._get_db_url(context)
        if not db_url:
            context.error("BackendGenerator: No database service named 'db' found")
            return

        text = self._renderer.render("app.py", {
            "db_url": db_url,
            "controllers": context.backend_app.controllers
        })
        context.write_out_file("services/backend/app.py", text)

    def generate_modules(self, context: RunContext):
        for entity in context.backend_app.entities:
            python_entity = self.convert_to_python_entity(entity, context)
            module_name = python_entity['_module_name']
            context.create_out_file(f"services/backend/modules/{module_name}/__init__.py")

            self._generate_module_entity(entity, python_entity, module_name, context)
            self._generate_module_repository(entity, python_entity, module_name, context)
            self._generate_module_service(entity, python_entity, module_name, context)
            self._generate_module_controller(entity, python_entity, module_name, context)

    def _generate_module_entity(self, entity, python_entity, module_name, context):
        text = self._renderer.render(f"module/entity.py", {
            "entity": python_entity
        })
        context.write_out_file(f"services/backend/modules/{module_name}/entity.py", text)

    def _generate_module_repository(self, entity, python_entity, module_name, context):
        text = self._renderer.render(f"module/repository.py", {
            "entity": python_entity
        })
        context.write_out_file(f"services/backend/modules/{module_name}/repository.py", text)

    def _generate_module_service(self, entity, python_entity, module_name, context):
        text = self._renderer.render(f"module/service.py", {
            "entity": python_entity,
            "service": entity.related_service
        })
        context.write_out_file(f"services/backend/modules/{module_name}/service.py", text)

    def _generate_module_controller(self, entity, python_entity, module_name, context: RunContext):
        # we need one controller per entity
        text = self._renderer.render(f"module/controller.py", {
            "entity": python_entity,
            "controller": entity.related_controller
        })
        context.write_out_file(f"services/backend/modules/{module_name}/controller.py", text)

    def convert_to_python_entity(self, entity: Entity, context: RunContext):
        # Convert the entity to a Python dictionary format
        python_entity = {
            "name": entity.name,
            "fields": [],

            "_table_name": entity.related_sql_table.name,
            "_module_name": to_snake_case(entity.name),
            "_entity": entity
        }
        for attr in entity.attributes:
            python_entity["fields"].append({
                "name": attr.name,
                "type": self._convert_to_python_type(attr.type),
                # "required": attr.required,
                "primary_key": attr == entity.id,
                # "auto_increment": attr.auto_increment,
                # "default": attr.default
                "_table_column": attr.related_sql_column
            })
        return python_entity

    def _convert_to_python_type(self, field_type: str):
        return "int" if field_type == "integer" else \
                "str"

    def _get_db_url(self, context: RunContext):
        db_service = context.containerized_services.get("db")
        if not db_service:
            return None

        env = getattr(db_service, "environment", {}) or {}
        user = env.get("POSTGRES_USER", "admin")
        pwd = env.get("POSTGRES_PASSWORD", "adminpass")
        db = env.get("POSTGRES_DB", "prototypo")
        host = "db"
        port = 5432
        return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    def generate_dockerfile(self, context: RunContext):
        text = self._renderer.render("Dockerfile", {})
        context.write_out_file("services/backend/Dockerfile", text)

    def generate_requirements_txt(self, context: RunContext):
        text = self._renderer.render("requirements.txt", {})
        context.write_out_file("services/backend/requirements.txt", text)

