from fastapi.testclient import TestClient
from app.main import app
from app.services import product_service
from app.auth.dependencies import get_current_user
from app.auth.dependencies import require_manager_or_admin

client = TestClient(app)

async def fake_current_user():
    return {
        "username": "jordy",
        "role": "ADMIN"
    }

async def fake_list_products(limit=10, offset=0, is_active=None, name=None, sku=None):
    return [
        {
            "id": 20260001,
            "display_id": "2026-0001",
            "sku": "SKU001",
            "name": "Produto Teste",
            "description": "Teste",
            "price": 10.5,
            "stock": 5,
            "is_active": True,
            "created_at": "2026-01-01T00:00:00",
            "updated_at": "2026-01-01T00:00:00",
        }
    ]


def test_get_products(monkeypatch):
    monkeypatch.setattr(product_service, "list_products", fake_list_products)
    
    app.dependency_overrides[get_current_user] = fake_current_user

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["sku"] == "SKU001"
    
async def fake_create_product(product):
    return {
        "id": 20260002,
        "display_id": "2026-0002",
        "message": "Produto criado com sucesso!"
    }


def test_create_product(monkeypatch):
    monkeypatch.setattr(product_service, "create_product", fake_create_product)

    payload = {
        "sku": "SKU002",
        "name": "Produto Teste",
        "description": "Produto criado em teste",
        "price": 20.5,
        "stock": 10
    }
    
    app.dependency_overrides[require_manager_or_admin] = fake_current_user

    response = client.post("/products", json=payload)

    assert response.status_code == 200
    assert response.json()["id"] == 20260002
    assert response.json()["display_id"] == "2026-0002"
    
from app.services import product_service

async def fake_get_product_by_id_none(product_id):
    return None

async def fake_get_product_by_id_success(product_id):
    return {
        "id": 20260001,
        "display_id": "2026-0001",
        "sku": "SKU001",
        "name": "Mouse",
        "price": 19.99,
        "stock": 10
    }


def test_get_product_not_found(monkeypatch):
    monkeypatch.setattr(
        product_service,
        "get_product_by_id",
        fake_get_product_by_id_none
    )
    
    app.dependency_overrides[require_manager_or_admin] = fake_current_user

    response = client.get("/products/99999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Produto não encontrado"
    }


def test_get_product_by_id(monkeypatch):
    monkeypatch.setattr(
        product_service,
        "get_product_by_id",
        fake_get_product_by_id_success
    )
    
    app.dependency_overrides[require_manager_or_admin] = fake_current_user

    response = client.get("/products/20260001")

    assert response.status_code == 200
    assert response.json()["sku"] == "SKU001"