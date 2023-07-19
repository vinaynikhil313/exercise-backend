DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
   id uuid PRIMARY KEY,
   created_at TIMESTAMP NOT NULL,
   order_type VARCHAR (20),
   side VARCHAR (20),
   instrument VARCHAR (12),
   limit_price FLOAT,
   quantity INT,
   status VARCHAR(20)
);
