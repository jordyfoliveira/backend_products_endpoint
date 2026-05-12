-- products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP NOT NULL DEFAULT NOW(),
    action TEXT NOT NULL,
    entity TEXT NOT NULL,
    entity_id INTEGER,
    details JSONB
);

-- índices úteis
CREATE INDEX IF NOT EXISTS idx_products_name ON products (name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_ts ON audit_logs (ts);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity_id ON audit_logs (entity_id);