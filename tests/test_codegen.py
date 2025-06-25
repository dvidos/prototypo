from core.codegen.sql import generate_sql

def test_sql_generation():
    entities = [{'name': 'Customer', 'fields': ['Name', 'Email']}]
    sql = generate_sql(entities)
    assert "CREATE TABLE Customer" in sql
    assert "Name VARCHAR(255)" in sql
    assert "Email VARCHAR(255)" in sql
