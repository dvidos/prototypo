CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    fullname TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    item_id INTEGER REFERENCES items(id)
);

INSERT INTO customers (fullname, address) VALUES
    ('Alice Smith', '123 Main St'),
    ('Bob Jones', '456 Oak Ave')
ON CONFLICT DO NOTHING;

INSERT INTO items (name) VALUES
    ('Widget'),
    ('Gadget')
ON CONFLICT DO NOTHING;
