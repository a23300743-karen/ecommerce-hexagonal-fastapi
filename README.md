# E-commerce Hexagonal FastAPI

Backend de e-commerce en Python con FastAPI, MySQL y una estructura basada en Arquitectura Hexagonal.

## Arquitectura

```txt
app/
├── domain/          # Entidades y puertos del negocio
├── application/     # Servicios/casos de uso
├── infrastructure/  # Implementaciones tecnicas, MySQL y repositorios
├── adapters/        # API HTTP, routers y schemas
└── main.py
```

La regla principal del proyecto es que `domain` y `application` no dependen de FastAPI ni de MySQL. Los routers reciben requests HTTP y delegan la logica a servicios de aplicacion, que trabajan contra puertos.

## Funciones disponibles

### Products

- `POST /products/`
- `GET /products/`
- `GET /products/search?name=laptop`
- `GET /products/{product_id}`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`

### Buyers

- `POST /buyers/`
- `GET /buyers/`
- `GET /buyers/search?name=ana`
- `GET /buyers/{buyer_id}`
- `PUT /buyers/{buyer_id}`
- `DELETE /buyers/{buyer_id}`

### Orders

- `POST /orders/`
- `GET /orders/`
- `GET /orders/{order_id}`
- `GET /orders/{order_id}/items`
- `PATCH /orders/{order_id}/cancel`

Al crear una orden se descuenta stock del producto. Al cancelar una orden se restaura el stock de los items asociados.

Los `DELETE` de productos y compradores son eliminaciones logicas: cambian el `status` a `INACTIVE` para no romper el historial de ordenes.

## Validaciones principales

### Productos

- `name` no puede estar vacio.
- `description` no puede estar vacia.
- `price` debe ser mayor a 0.
- `stock` debe ser mayor o igual a 0.
- `status` solo puede ser `ACTIVE` o `INACTIVE`.

### Buyers

- `name` no puede estar vacio.
- `email` debe contener `@` y terminar en `.com`.
- `email` debe ser unico.
- `address` no puede estar vacia.
- `phone` es opcional, pero si existe debe tener minimo 10 digitos.
- `status` solo puede ser `ACTIVE` o `INACTIVE`.

### Orders

- `buyer_id` debe existir.
- El comprador debe estar `ACTIVE`.
- `product_id` debe existir.
- El producto debe estar `ACTIVE`.
- `quantity` debe ser mayor a 0.
- Debe existir stock suficiente.
- No se puede cancelar una orden inexistente.
- No se puede cancelar una orden ya cancelada.

## Requisitos

- Python 3.11+
- MySQL

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuracion

La conexion a MySQL usa variables de entorno opcionales:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=ecommerce
```

Si no defines variables, se usan esos valores por defecto.

## Base de datos MySQL

El proyecto esta preparado para trabajar con la base `ecommerce`. La estructura actual manejada por el proyecto es compatible con el archivo `ecommerce.sql`.

```sql
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) DEFAULT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS buyer_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'CREATED',
    total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES buyer_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

> Nota: la base permite `products.description` como `NULL`, pero la API lo solicita al crear productos para mantener una ficha de producto mas completa.

Si ya tienes creada la tabla `buyer_profiles` sin `status`, ejecuta:

```sql
ALTER TABLE buyer_profiles
ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

Swagger:

```txt
http://localhost:8000/docs
```

## Ejemplos

Crear producto:

```json
{
  "name": "Laptop",
  "description": "Laptop para desarrollo",
  "price": 15000,
  "stock": 5
}
```

Crear comprador:

```json
{
  "name": "Ana Lopez",
  "email": "ana@example.com",
  "address": "Av. Central 123",
  "phone": "5551234567"
}
```

Crear orden:

```json
{
  "buyer_id": 1,
  "product_id": 1,
  "quantity": 2
}
```
