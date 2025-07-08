import os
from core.template import TemplateRenderer
from core.plugin_registration import PluginRegistration, SystemHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from core.model.service_definition import ServiceDefinition


class ReactAppGeneratorPlugin:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self._renderer = TemplateRenderer(template_dir)

    def register(self):
        return PluginRegistration(
            name="React App Generator",
            system_hooks=[
                SystemHook(CompilerPhase.SYS_INIT, self.on_init),
                SystemHook(CompilerPhase.SYS_GENERATE_OUT, self.on_generate)
            ]
        )

    def on_init(self, blocks, context: RunContext):
        # we could validate if we have any entities first
        context.add_containerized_service(ServiceDefinition(
            name="frontend",
            build_path="services/frontend",
            dockerfile="Dockerfile",
            ports=["8000:80"],
            depends_on=["backend"]
        ))

    def on_generate(self, blocks, context: RunContext):
        self.generate_react_app(context)
        self.generate_dockerfile(context)
        self.generate_package_json(context)
        self.generate_public_html(context)
        self.generate_index_js(context)

    def generate_react_app(self, context: RunContext):
        text = self._renderer.render("src/App.js", {
            "app": context.frontend_app
        })
        context.write_out_file("services/frontend/src/App.js", text)

    def generate_dockerfile(self, context: RunContext):
        text = self._renderer.render("Dockerfile", {})
        context.write_out_file("services/frontend/Dockerfile", text)

    def generate_package_json(self, context: RunContext):
        text = self._renderer.render("package.json", {})
        context.write_out_file("services/frontend/package.json", text)

    def generate_public_html(self, context: RunContext):
        text = self._renderer.render("public/index.html", {})
        context.write_out_file("services/frontend/public/index.html", text)

    def generate_index_js(self, context: RunContext):
        text = self._renderer.render("src/index.js", {})
        context.write_out_file("services/frontend/src/index.js", text)

