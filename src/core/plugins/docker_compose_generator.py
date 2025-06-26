import os
import yaml
from core.plugin_manager import PluginRegistration
from core.run_context import RunContext

class SamplePlugin:
    def register(self):
        return PluginRegistration(
            name="Database Generator",
            block_types=[],
            hooks={
                "on_init": self.on_init,
                "validate": self.validate,
                "transform": self.transform,
                "generate": self.generate,
                "on_finalize": self.on_finalize
            }
        )

    def on_init(self, blocks, context: RunContext):
        ...

    def validate(self, block, context: RunContext):
        ...

    def transform(self, block, context: RunContext):
        ...

    def generate(self, block, context: RunContext):
        ...

    def on_finalize(self, blocks, context: RunContext):
        services = {}
        for svc in context.services.values():
            service = {}
            if svc.build_path:
                service["build"] = {
                    "context": svc.build_path
                }
                if svc.dockerfile:
                    service["build"]["dockerfile"] = svc.dockerfile
            if svc.image:
                service["image"] = svc.image
            if svc.ports:
                service["ports"] = svc.ports
            if svc.environment:
                service["environment"] = svc.environment
            if svc.volumes:
                service["volumes"] = svc.volumes
            if svc.depends_on:
                service["depends_on"] = svc.depends_on
            if svc.command:
                service["command"] = svc.command

            services[svc.name] = service

        compose = {
            "services": services
        }

        if (len(context.volumes) > 0):
            compose['volumes'] = {}
            for volume in context.volumes:
                compose['volumes'][volume] = None

        os.makedirs(context.out_dir, exist_ok=True)
        compose_path = os.path.join(context.out_dir, "docker-compose.yml")
        with open(compose_path, "w") as f:
            yaml.dump(compose, f, sort_keys=False)

        context.print(f"✅ Docker Compose written to: {compose_path}")

