
def generate_sql(blocks):
    sql_statements = []
    for block in blocks:
        cols = ["  id INT PRIMARY KEY AUTO_INCREMENT"]
        for field in block['assignments']:
            cols.append(f"  {field['name']} VARCHAR(255)")
        sql = f"CREATE TABLE {block['name']} (\n" + ",\n".join(cols) + "\n);"
        sql_statements.append(sql)
    return "\n\n".join(sql_statements)
