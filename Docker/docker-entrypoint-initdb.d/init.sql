 -- docker-entrypoint-initdb.d/init.sql

CREATE TABLE inventory_warehouse (
  id serial PRIMARY KEY,
  name varchar(200) NOT NULL,
  location varchar(300) NOT NULL,
  capacity integer NOT NULL
);

CREATE TABLE inventory_inventory (
  id serial PRIMARY KEY,
  warehouse_id integer NOT NULL REFERENCES inventory_warehouse(id) ON DELETE CASCADE,
  product_sku varchar(50) NOT NULL,
  product_name varchar(200) NOT NULL,
  quantity integer NOT NULL,
  UNIQUE (warehouse_id, product_sku)
);

-- Now insert your data

INSERT INTO inventory_warehouse (id, name, location, capacity)
VALUES (1, 'Central Depot', 'Colombo', 5000),
       (2, 'Secondary Hub', 'Kandy', 3000);

INSERT INTO inventory_inventory (id, warehouse_id, product_sku, product_name, quantity)
VALUES (1, 1, 'SKU123', 'Widget A', 250),
       (2, 1, 'SKU456', 'Gadget B', 100),
       (3, 2, 'SKU789', 'Widget C', 400),
       (4, 1, 'SKU790', 'Widget D', 400);
