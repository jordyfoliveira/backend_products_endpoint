````md
# Products Async API

Async REST API developed with FastAPI, PostgreSQL and psycopg.

This project was created as a backend practice project focused on:
- asynchronous programming
- layered architecture
- PostgreSQL integration
- audit logs
- soft delete
- filtering and pagination
- custom exception handling
- Dockerized development environment

---

# Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- psycopg3
- Docker & Docker Compose
- Pydantic

---

# Features

## Products

- Create products
- List products
- Get product by ID
- Update stock
- Update price
- Activate product
- Deactivate product
- Delete inactive products

## Extra Features

- Custom product IDs
- Display IDs formatted as `YYYY-NNNN`
- Pagination
- Filters
- Audit logs
- Automatic timestamps
- Global exception handlers
- Soft delete system

---

# Project Structure

```text
app/
├── db/
├── exceptions/
├── repositories/
├── routers/
├── schemas/
├── services/
├── utils/
└── main.py
````

---

# Product ID System

Products use an internal numeric ID format:

```text
20260001
```

Displayed externally as:

```text
2026-0001
```

---

# API Endpoints

## Health

### Health Check

```http
GET /health
```

### Database Health Check

```http
GET /db-health
```

---

# Products

## List Products

```http
GET /products
```

### Query Parameters

| Parameter   | Type | Description                     |
| ----------- | ---- | ------------------------------- |
| limit       | int  | Number of results               |
| offset      | int  | Pagination offset               |
| is_active   | bool | Filter active/inactive products |
| name_filter | str  | Filter by product name          |
| sku_filter  | str  | Filter by SKU                   |

### Examples

```http
GET /products?limit=5&offset=0
```

```http
GET /products?is_active=true
```

```http
GET /products?name_filter=mouse
```

---

## Get Product By ID

```http
GET /products/{product_id}
```

---

## Create Product

```http
POST /products
```

### Request Body

```json
{
  "sku": "SKU001",
  "name": "Gaming Mouse",
  "description": "Wireless gaming mouse",
  "price": 59.99,
  "stock": 10
}
```

---

## Update Product Stock

```http
PATCH /products/{product_id}/stock
```

### Request Body

```json
{
  "stock": 20
}
```

---

## Update Product Price

```http
PATCH /products/{product_id}/price
```

### Request Body

```json
{
  "price": 99.99
}
```

---

## Deactivate Product

```http
PATCH /products/{product_id}/deactivate
```

---

## Activate Product

```http
PATCH /products/{product_id}/activate
```

---

## Delete Product

A product must be deactivated before deletion.

```http
DELETE /products/{product_id}
```

---

# Audit Logs

Every important action is logged in the `audit_logs` table.

Examples:

* product creation
* stock updates
* price updates
* activation/deactivation
* deletion

---

# Validation Rules

## SKU

Format:

```text
SKU001
```

## Price

* must be greater than 0

## Stock

* must be greater than or equal to 0

---

# Running with Docker

## Start containers

```bash
docker compose up --build
```

## Stop containers

```bash
docker compose down
```

## Remove volumes

```bash
docker compose down -v
```

---

# Environment Variables

Create a `.env` file:

```env
POSTGRES_HOST=db
POSTGRES_DB=products_db
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_PORT=5432
```

---

# Future Improvements

* JWT authentication
* Role-based permissions
* Alembic migrations
* Automated tests
* Sorting
* Audit log endpoints
* Response schemas
* Search improvements

---

# Author

Jordy Oliveira

```
```
