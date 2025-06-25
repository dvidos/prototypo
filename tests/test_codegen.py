from core.codegen.sql import generate_sql

def test_sql_generation():
    blocks = [{'name': 'Customer', 'assignments': [
        {'name': 'Name'},
        {'name':'Email'}
    ]}]
    sql = generate_sql(blocks)
    assert "CREATE TABLE Customer" in sql
    assert "Name VARCHAR(255)" in sql
    assert "Email VARCHAR(255)" in sql
