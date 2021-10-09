-- Enable UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS client (
    client_id uuid DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    PRIMARY KEY (client_id)
);

CREATE TABLE IF NOT EXISTS item_collection (
    collection_id uuid DEFAULT uuid_generate_v4(),
    client_id uuid NOT NULL,
    name VARCHAR NOT NULL,
    PRIMARY KEY (collection_id),
    CONSTRAINT fk_client_id FOREIGN KEY (client_id) REFERENCES client (client_id)
);

CREATE TABLE IF NOT EXISTS item_type (
    item_type_id uuid DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    PRIMARY KEY(item_type_id) 
);

CREATE TABLE IF NOT EXISTS item (
    item_id uuid DEFAULT uuid_generate_v4(),
    collection_id uuid NOT NULL,
    item_type_id uuid NOT NULL,
    quantitiy integer NOT NULL,
    PRIMARY KEY (item_id),
    CONSTRAINT fk_collection_id FOREIGN KEY (collection_id) REFERENCES item_collection (collection_id),
    CONSTRAINT fk_item_type_id FOREIGN KEY (item_type_id) REFERENCES item_type (item_type_id)
);