
def generate_sql(entities):
    sql_statements = []
    for entity in entities:
        cols = ["  id INT PRIMARY KEY AUTO_INCREMENT"]
        for field in entity['fields']:
            cols.append(f"  {field} VARCHAR(255)")
        sql = f"CREATE TABLE {entity['name']} (\n" + ",\n".join(cols) + "\n);"
        sql_statements.append(sql)
    return "\n\n".join(sql_statements)
