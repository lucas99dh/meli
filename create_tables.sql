-- Tabla customer
CREATE TABLE customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    sexo CHAR(1),
    direccion VARCHAR(255),
    fecha_nacimiento DATE,
    telefono VARCHAR(20)
);

-- Tabla category
CREATE TABLE category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    path VARCHAR(255) NOT NULL
);

-- Tabla item
CREATE TABLE item (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    seller_id INT NOT NULL,
    category_id INT NOT NULL,
    nombre VARCHAR(100),
    precio DECIMAL(10,2) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_publicacion DATE,
    fecha_baja DATE
);

-- Tabla orders
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    fecha_order DATE NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

-- Tabla item_Status
CREATE TABLE item_Status (
    item_id INT PRIMARY KEY,
    precio DECIMAL(10,2) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL
);