-- db/init.sql

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    address TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    total NUMERIC(12, 2) NOT NULL,
    amount_paid NUMERIC(12, 2) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending'
);

CREATE TABLE order_lines (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku VARCHAR(50) NOT NULL,
    description TEXT,
    qty INTEGER NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    ext_price NUMERIC(12, 2) NOT NULL
);

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_type TEXT NOT NULL,
  aggregate_id UUID NOT NULL,
  type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE PUBLICATION appdb_pub FOR TABLE events;
ALTER ROLE postgres WITH REPLICATION;
