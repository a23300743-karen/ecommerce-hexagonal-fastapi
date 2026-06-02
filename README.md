# E-commerce Hexagonal FastAPI

Backend de e-commerce en Python con FastAPI, MySQL, OAuth2/JWT y WebSockets usando Arquitectura Hexagonal.

## Arquitectura

```txt
app/
|-- domain/          # Entidades y puertos del negocio
|-- application/     # Servicios/casos de uso
|-- infrastructure/  # MySQL, seguridad JWT/bcrypt y FAQ
|-- adapters/        # API HTTP, schemas y WebSockets
|-- realtime/        # Manejo de conexiones WebSocket
`-- main.py
```

La regla principal del proyecto es que `domain` y `application` no dependen de FastAPI, MySQL, JWT, bcrypt ni WebSockets. Los adapters conectan el exterior con los casos de uso.

## Endpoints

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

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

### Realtime Chat

- `WS /ws/chat`

## Autenticacion y autorizacion

El proyecto implementa OAuth2 con Bearer Token y JWT:

1. El usuario se registra en `/auth/register`.
2. El usuario inicia sesion en `/auth/login`.
3. El backend valida email y contrasena hasheada.
4. El backend genera un `access_token` JWT y un `refresh_token` JWT.
5. El cliente manda el `access_token` en `Authorization: Bearer <token>`.
6. Cuando el `access_token` expira, el cliente usa `/auth/refresh`.

Endpoints protegidos:

- `POST /products/`: requiere `ADMIN`.
- `PUT /products/{product_id}`: requiere `ADMIN`.
- `DELETE /products/{product_id}`: requiere `ADMIN`.
- `POST /orders/`: requiere usuario autenticado.
- `PATCH /orders/{order_id}/cancel`: requiere usuario autenticado.
- `GET /auth/me`: requiere usuario autenticado.

Endpoints publicos:

- `GET /products/`
- `GET /products/search?name=...`
- `GET /products/{product_id}`

## Chat cliente-asistente con WebSockets

El chat de soporte funciona en tiempo real:

```txt
ws://localhost:8000/ws/chat
```

El cliente puede enviar texto simple:

```txt
estado de mi orden
```

O un mensaje JSON:

```json
{
  "user": "client",
  "content": "Que metodos de pago aceptan?"
}
```

Respuesta FAQ:

```json
{
  "type": "faq",
  "message": {
    "id": null,
    "user": "client",
    "content": "Que metodos de pago aceptan?",
    "created_at": "2026-05-31T00:00:00+00:00"
  },
  "response": "Por ahora aceptamos pagos registrados por el sistema. La integracion con pasarela de pago puede agregarse como adapter externo."
}
```

Si no hay coincidencia:

```json
{
  "type": "support",
  "response": "Tu mensaje fue enviado a soporte. Un asistente lo revisara pronto."
}
```

FAQs detectadas:

- estado de ordenes
- metodos de pago
- tiempos de envio
- horarios de atencion
- cancelacion de ordenes
- stock y disponibilidad

Arquitectura del chat:

```txt
domain/models/message.py              # Entidad Message
domain/ports/faq_port.py              # Contrato FAQPort
application/services/chat_service.py  # Caso de uso del chat
infrastructure/faq/                   # Motor FAQ en memoria
realtime/connection_manager.py        # Manejo de conexiones WebSocket
adapters/websocket/chat_socket.py     # Adapter WebSocket de FastAPI
```

La logica FAQ esta desacoplada por `FAQPort`. En el futuro se puede reemplazar `FAQMemoryRepository` por MySQL, Redis, embeddings, RAG, OpenAI/LLM o un repositorio de conocimiento externo.


## Imagenes de productos

Los productos pueden crearse y actualizarse con una imagen subida desde la computadora. El backend recibe `multipart/form-data`, guarda el archivo en `uploads/products/` y devuelve `image_url`.

El frontend usa esa URL para mostrar la imagen real del producto. Si un producto no tiene imagen, se usa una imagen local por defecto segun el nombre.

Al editar un producto, si no eliges una imagen nueva, se conserva la imagen anterior.

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

Variables de entorno opcionales para MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=ecommerce
```

Variables opcionales para JWT:

```env
JWT_SECRET_KEY=CAMBIA_ESTA_CLAVE_SECRETA
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Base de datos

Si ya tienes creada la tabla `buyer_profiles` sin `status`, ejecuta:

```sql
ALTER TABLE buyer_profiles
ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';
```


Para habilitar imagenes de productos en una base existente, ejecuta:

```sql
ALTER TABLE products
ADD COLUMN image_url VARCHAR(255) DEFAULT NULL;
```

Para autenticacion ejecuta:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'CUSTOMER',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
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

Registrar admin:

```json
{
  "name": "Admin",
  "email": "admin@email.com",
  "password": "123456",
  "role": "ADMIN"
}
```

Login OAuth2 en Swagger:

```txt
username: admin@email.com
password: 123456
```

Respuesta de login:

```json
{
  "access_token": "TOKEN_CORTO",
  "refresh_token": "TOKEN_LARGO",
  "token_type": "bearer"
}
```

Renovar access token:

```json
{
  "refresh_token": "TOKEN_LARGO"
}
```

Crear producto:

```json
{
  "name": "Laptop",
  "description": "Laptop para desarrollo",
  "price": 15000,
  "stock": 5,
  "status": "ACTIVE"
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
