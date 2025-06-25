class SqlGeneratorPlugin:
    def register(self):
        return {
            "name": "SQL Generator",
            "block_types": ["entity"],
            "hooks": {
                "on_block": self.on_entity
            }
        }

    def on_entity(self, block, context):
        print(f"[SQL Plugin] Processing entity: {block['name']}")

    def _generate_sql(block):
        sql_statements = []
        cols = ["  id INT PRIMARY KEY AUTO_INCREMENT"]
        for field in block['assignments']:
            cols.append(f"  {field['name']} VARCHAR(255)")
        sql = f"CREATE TABLE {block['name']} (\n" + ",\n".join(cols) + "\n);"
        sql_statements.append(sql)
        return "\n\n".join(sql_statements)
