from app.schemas.product import ProductCreate
import pytest
from pydantic import ValidationError

def test_product_create():
    product = ProductCreate(sku="SKU001", name="Mouse", description="Mouse sem fios", price=29.99, stock=10)
    assert product.sku == "SKU001"

def test_invalid_sku():
    with pytest.raises(ValidationError):
        ProductCreate(sku="ABC123", name="Mouse", description="Mouse sem fios", price=29.99, stock=10)
