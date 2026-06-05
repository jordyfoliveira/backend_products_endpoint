from fastapi.testclient import TestClient
from app.main import app
from app.services import product_service

client = TestClient(app)


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

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["sku"] == "SKU001"