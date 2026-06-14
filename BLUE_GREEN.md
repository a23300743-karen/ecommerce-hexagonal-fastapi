# Despliegue Blue/Green del E-commerce

## Arquitectura

```text
Navegador
   |
   v
Nginx :8080
   |
   +--> BLUE  app_blue:8000  version 2.0.0
   |
   `--> GREEN app_green:8000 version 2.1.0
              |
              v
          MySQL compartido
```

Nginx es la unica entrada publica. Los puertos `8001` y `8002` se exponen en
localhost solamente para validar cada candidato durante la practica.

- **Blue 2.0.0:** version estable con los colores actuales y checkout directo.
- **Green 2.1.0:** version candidata con tema verde, aviso visual y resumen de
  confirmacion del checkout.
- **MySQL:** compartido para conservar usuarios, productos y ordenes al cambiar trafico.
- **Uploads:** volumen compartido para que las imagenes existan en ambas versiones.

## Archivos

```text
blue/
|-- Dockerfile
`-- release.env
green/
|-- Dockerfile
`-- release.env
nginx/
|-- nginx.conf
|-- active-upstream.inc
|-- blue-upstream.inc
|-- green-upstream.inc
`-- active-environment
scripts/
|-- promote.sh
|-- rollback.sh
|-- status.sh
|-- promote.ps1
`-- rollback.ps1
docker-compose.yml
```

## Inicio

En Docker Desktop debe estar activo el motor Linux. Desde la raiz del proyecto:

```bash
docker compose up -d --build
```

Verificar:

```bash
docker compose ps
curl http://localhost:8001/deployment
curl http://localhost:8002/deployment
curl http://localhost:8080/deployment
```

Abrir la aplicacion mediante Nginx:

```text
http://localhost:8080
```

Al inicio, `active-upstream.inc` apunta a Blue.

## Promocion Blue a Green

Desde Git Bash:

```bash
./scripts/promote.sh green
```

Desde PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/promote.ps1 -Target green
```

El script:

1. Construye y levanta Green.
2. Espera una respuesta correcta de `http://localhost:8002/health`.
3. No modifica Nginx si Green falla.
4. Cambia atomicamente el upstream activo.
5. Ejecuta `nginx -t`.
6. Recarga Nginx con `nginx -s reload` sin detener el proxy.
7. Comprueba por `:8080/deployment` que Green recibe las nuevas peticiones.

Recarga el navegador. La etiqueta inferior debe cambiar de `BLUE 2.0.0` a
`GREEN 2.1.0`. En Green, el encabezado cambia a verde, aparece el aviso de
version candidata y Finalizar compra abre el resumen de confirmacion.

## Rollback

Git Bash:

```bash
./scripts/rollback.sh
```

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/rollback.ps1
```

El rollback valida el ambiente anterior y vuelve a recargar Nginx. Los
contenedores no se apagan durante el cambio, por lo que no existe downtime del
proxy.

## Demostracion de promocion rechazada

Para simular una version Green defectuosa, agregar temporalmente a
`green/release.env`:

```env
FORCE_UNHEALTHY=true
```

Ejecutar de nuevo la promocion. El health check respondera `503`, el script
terminara con error y Nginx seguira apuntando a Blue. Despues eliminar esa linea
o cambiarla por `false`, reconstruir Green y promover normalmente.

## Base de datos

No es necesario cambiar tablas para Blue/Green. Docker crea una base propia
usando `ecommerce.sql` la primera vez que se crea el volumen.

Importante:

- Si quieres usar los datos actuales de phpMyAdmin, exportalos primero a
  `ecommerce.sql` antes del primer `docker compose up`.
- Los scripts de `/docker-entrypoint-initdb.d` solo se ejecutan cuando el volumen
  de MySQL esta vacio.
- Blue y Green deben usar cambios de esquema compatibles entre ambas versiones.
- No uses `docker compose down -v` durante una demostracion, porque `-v` elimina
  la base y las imagenes almacenadas en volumen.

## Evidencias recomendadas

1. `docker compose ps` con Blue, Green, MySQL y Nginx saludables.
2. Navegador mostrando `BLUE 2.0.0` en `http://localhost:8080`.
3. Respuesta de `http://localhost:8001/deployment` y `:8002/deployment`.
4. Ejecucion de `promote.sh green` o `promote.ps1 -Target green`.
5. Navegador mostrando `GREEN 2.1.0` y el checkout con confirmacion.
6. Ejecucion del rollback.
7. Navegador nuevamente en Blue con el e-commerce funcionando.
8. Opcional: promocion rechazada usando `FORCE_UNHEALTHY=true`.

## Limpieza sin borrar datos

```bash
docker compose down
```

Para volver a levantar:

```bash
docker compose up -d
```
