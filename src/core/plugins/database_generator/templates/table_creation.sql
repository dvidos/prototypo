
CREATE TABLE IF NOT EXISTS {{ table.name }} (
    {% for column in table.columns %}
    {{ column.name }} {{ column.type }}{{ ' PRIMARY KEY' if column.primary_key else '' }}{{ ' NOT NULL' if column.not_null else '' }}{{ ',' if not loop.last else '' }}
    {% endfor %}
);

{% for table in foreign_keys %}
ALTER TABLE {{ table.name }} ADD CONSTRAINT {{ table.constraint_name }} FOREIGN KEY ({{ table.column }}) REFERENCES {{ table.referenced_table }}({{ table.referenced_column }});
{% endfor %}

{% for index in table.indexes %}
CREATE INDEX IF NOT EXISTS idx_{{ index.name }} ON {{ table.name }} ({{ index.columns | join(', ') }});
{% endfor %}

{% for insert in inserts %}
INSERT INTO {{ insert.table }} ({{ insert.columns | join(', ') }}) VALUES
    {% for row in insert.rows %}
        ({{ row | join(', ') }}){{ ',' if not loop.last else '' }}
    {% endfor %}
ON CONFLICT DO NOTHING;
{% endfor %}
