import os
from core.template import TemplateRenderer
from core.plugin_registration import PluginRegistration, SystemHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from core.model.service_definition import ServiceDefinition


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
        context.add_service(ServiceDefinition(
            name="backend",
            build_path="services/backend",
            dockerfile="Dockerfile",
            ports=["8080:8080"],
            depends_on=["db"]
        ))

    def on_generate(self, blocks, context: RunContext):
        self.generate_app_py(context)
        self.generate_controllers(context)
        self.generate_requirements_txt(context)
        self.generate_dockerfile(context)

    def generate_app_py(self, context: RunContext):
        db_url = self.get_db_url(context)
        if not db_url:
            context.error("BackendGenerator: No database service named 'db' found")
            return

        text = self._renderer.render("app.py", {
            "db_url": db_url,
            "controllers": context.backend_app.controllers
        })
        context.write_out_file("services/backend/app.py", text)
        context.create_out_file("services/backend/controllers/__init__.py")

    def generate_controllers(self, context: RunContext):
        for controller in context.backend_app.controllers:
            text = self._renderer.render("controller.py", {
                "controller": controller
            })
            context.write_out_file(f"services/backend/controllers/{controller.name.lower()}.py", text)


    def get_db_url(self, context: RunContext):
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

