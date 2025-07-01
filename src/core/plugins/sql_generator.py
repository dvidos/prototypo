from core.plugin_manager import PluginRegistration

class SqlGeneratorPlugin:
    def register(self):
        return PluginRegistration(
            name="Sql Generator Plugin",
            block_types=['entity'],
            hooks={
                "generate": self.generate
            }
        )

    def generate(self, block, context):
        # print(f"[SQL Plugin] Processing entity: {block.name}")
        # print(self._generate_sql(block))
        ...

    def _generate_sql(self, block):
        sql_statements = []
        cols = ["  id INT PRIMARY KEY AUTO_INCREMENT"]
        for field in block.assignments:
            cols.append(f"  {field.name} VARCHAR(255)")
        sql = f"CREATE TABLE {block.name} (\n" + ",\n".join(cols) + "\n);"
        sql_statements.append(sql)
        return "\n\n".join(sql_statements)
