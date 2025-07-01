from core.plugin_registration import PluginRegistration, SystemHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from core.model.service_definition import ServiceDefinition


class DatabaseGeneratorPlugin:
    def register(self):
        return PluginRegistration(
            name="Database Generator",
            system_hooks=[
                SystemHook(CompilerPhase.SYS_INIT, self.on_init),
                SystemHook(CompilerPhase.SYS_FINALIZE, self.on_finalize)
            ]
        )

    def on_init(self, blocks, context: RunContext):
        # we could validate if we have any entities first
        context.add_service(ServiceDefinition(
            name="db",
            image="postgres:15",
            ports=["5432:5432"],
            environment={
                "POSTGRES_USER": "admin",
                "POSTGRES_PASSWORD": "adminpass",
                "POSTGRES_DB": "prototypo"
            },
            volumes=["pgdata:/var/lib/postgresql/data"],
            depends_on=[],
        ))
        context.add_volume("pgdata")

    def validate(self, block, context: RunContext):
        ...

    def transform(self, block, context: RunContext):
        ...

    def generate(self, block, context: RunContext):
        ...

    def on_finalize(self, blocks, context: RunContext):
        ...
