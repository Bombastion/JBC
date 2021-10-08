-- Enable UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS client (
    client_id uuid DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    PRIMARY KEY (client_id)
);

CREATE TABLE IF NOT EXISTS CELLAR (
    cellar_id uuid DEFAULT uuid_generate_v4(),
    client_id uuid NOT NULL,
    name VARCHAR NOT NULL,
    PRIMARY KEY (cellar_id),
    CONSTRAINT fk_user_id FOREIGN KEY (client_id) REFERENCES client (client_id)
);

CREATE TABLE IF NOT EXISTS product (
    product_id uuid DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    PRIMARY KEY(product_id) 
);

CREATE TABLE IF NOT EXISTS beer (
    beer_id uuid DEFAULT uuid_generate_v4(),
    cellar_id uuid NOT NULL,
    product_id uuid NOT NULL,
    name VARCHAR NOT NULL,
    PRIMARY KEY (cellar_id),
    CONSTRAINT fk_cellar_id FOREIGN KEY (cellar_id) REFERENCES cellar (cellar_id),
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES product (product_id)
);