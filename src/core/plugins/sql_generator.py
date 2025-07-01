from core.plugin_registration import PluginRegistration


class SqlGeneratorPlugin:
    def register(self):
        return PluginRegistration(
            name="Sql Generator Plugin"
        )

    def _generate_sql(self, block):
        sql_statements = []
        cols = ["  id INT PRIMARY KEY AUTO_INCREMENT"]
        for field in block.assignments:
            cols.append(f"  {field.name} VARCHAR(255)")
        sql = f"CREATE TABLE {block.name} (\n" + ",\n".join(cols) + "\n);"
        sql_statements.append(sql)
        return "\n\n".join(sql_statements)
