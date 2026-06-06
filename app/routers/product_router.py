from fastapi import APIRouter, Query
from app.exceptions.custom_exceptions import DuplicateSKUError, ProductActiveError, ProductNotFoundError
from app.services import product_service
from app.schemas.product import ProductCreate, StockUpdate, PriceUpdate
from fastapi import Depends
from app.auth.dependencies import get_current_user, require_admin, require_manager_or_admin

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("")
async def get_products(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), is_active: bool | None = None, name: str | None = None, sku: str | None = None, current_user = Depends(get_current_user)):
    return await product_service.list_products(limit, offset, is_active, name, sku)

@router.get("/{product_id}")
async def get_product(product_id: int, current_user = Depends(get_current_user)):
    product = await product_service.get_product_by_id(product_id)
    
    if product is None:
        raise ProductNotFoundError()
    
    return product

@router.post("")
async def create_product(product: ProductCreate, current_user = Depends(require_manager_or_admin)):
    product_id = await product_service.create_product(product, current_user["username"])
    
    if product_id == "DUPLICATE_SKU":
        raise DuplicateSKUError()
    
    return product_id

@router.patch("/{product_id}/stock")
async def update_stock(product_id: int, stock_update: StockUpdate, current_user = Depends(require_manager_or_admin)):
    new_stock = await product_service.update_stock(product_id, stock_update.stock, current_user["username"])
    
    if new_stock is None:
        raise ProductNotFoundError()
    
    return new_stock

@router.patch("/{product_id}/price")
async def update_price(product_id: int, price_update: PriceUpdate, current_user = Depends(require_manager_or_admin)):
    new_price = await product_service.update_price(product_id, price_update.price, current_user["username"])
    
    if new_price is None:
        raise ProductNotFoundError()
    
    return new_price

@router.patch("/{product_id}/deactivate")
async def deactivate_product(product_id: int, current_user = Depends(require_admin)):
    product = await product_service.deactivate_product(product_id, current_user["username"])
    
    if product is None:
        raise ProductNotFoundError()
    
    return product

@router.patch("/{product_id}/activate")
async def activate_product(product_id: int, current_user = Depends(require_admin)):
    product = await product_service.activate_product(product_id, current_user["username"])
    
    if product is None:
        raise ProductNotFoundError()
    
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int, current_user = Depends(require_admin)):
    product = await product_service.delete_product(product_id, current_user["username"])
    
    if product is None:
        raise ProductNotFoundError()
    
    if product == "ACTIVE":
        raise ProductActiveError()
    
    return product


#@router.get("/inactive")
#async def get_products_inactive():
#    return await product_service.get_products_inactive()

#@router.delete("/{product_id}/hard")
#async def hard_delete_product(product_id: int):
#    product = await product_service.hard_delete_product(product_id)
#    
#    if product is None:
#        raise ProductNotFoundError()
#    
#    return product