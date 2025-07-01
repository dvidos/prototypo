import os

from core.model.block import Block
from core.model.relational_schema.column import DataType
from core.template import TemplateRenderer
from core.plugin_registration import PluginRegistration, SystemHook, BlockHook
from core.compiler_phase import CompilerPhase
from core.run_context import RunContext
from core.model.service_definition import ServiceDefinition


class DatabaseGeneratorPlugin:

    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self._renderer = TemplateRenderer(template_dir)
        self._postgres_type_mapping = {
            DataType.STRING: 'VARCHAR',
            DataType.INT: 'INTEGER',
            DataType.FLOAT: 'REAL',
            DataType.BOOLEAN: 'BOOLEAN',
            DataType.DATE: 'DATE',
            DataType.TIMESTAMP: 'TIMESTAMP',
            DataType.JSON: 'JSONB'
        }

    def register(self):
        return PluginRegistration(
            name="Database Generator",
            system_hooks=[
                SystemHook(CompilerPhase.SYS_INIT, self.on_init),
                SystemHook(CompilerPhase.SYS_GENERATE_OUT, self.on_generate),
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
            volumes=[
                "pgdata:/var/lib/postgresql/data",
                "./services/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro"
            ],
            depends_on=[],
        ))
        context.add_volume("pgdata")

    def on_generate(self, blocks, context: RunContext):
        self.generate_init_sql(context)

    def generate_init_sql(self, context: RunContext):
        init = ""
        for table in context.db_schema.tables:
            postgres_table = {
                'name': table.name,
                'columns': [self._map_to_postgres_column(col) for col in table.columns],
                'indexes': table.indexes,
                'foreign_keys': table.foreign_keys,
            }
            text = self._renderer.render("table_creation.sql", { 'table': postgres_table })
            init += text + "\n"

        context.write_out_file("services/db/init.sql", init)

    def _map_to_postgres_column(self, column):
        if column.auto_increment:
            type = 'SERIAL'
        else:
            type = self._postgres_type_mapping.get(column.type.name, 'TEXT')

        return {
            'name': column.name,
            'type': type,
            'not_null': column.not_null,
            'default': column.default,
            'primary_key': column.primary_key,
            'auto_increment': column.auto_increment
        }
