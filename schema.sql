CREATE TABLE carriers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    dot_number VARCHAR(50) UNIQUE NOT NULL,
    mc_number VARCHAR(50),
    insurance_exp_date DATE,
    w9_status BOOLEAN DEFAULT FALSE,
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    billing_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE loads (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    carrier_id INTEGER REFERENCES carriers(id),
    pickup_location TEXT NOT NULL,
    delivery_location TEXT NOT NULL,
    pickup_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    rate_customer DECIMAL(10,2),
    rate_carrier DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE load_tracking (
    id SERIAL PRIMARY KEY,
    load_id INTEGER REFERENCES loads(id),
    status_update TEXT,
    location TEXT,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
