from fastapi import APIRouter, HTTPException
from app.services import product_service
from app.schemas.product import ProductCreate, StockUpdate, PriceUpdate

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("")
async def get_products():
    return await product_service.list_products()

@router.get("/inactive")
async def get_products_inactive():
    return await product_service.get_products_inactive()

@router.get("/{product_id}")
async def get_product(product_id: int):
    product = await product_service.get_product_by_id(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return product

@router.post("")
async def create_product(product: ProductCreate):
    product_id = await product_service.create_product(product)
    return {"id": product_id, "message": "Produto criado com sucesso!"}

@router.patch("/{product_id}/stock")
async def update_stock(product_id: int, stock_update: StockUpdate):
    new_stock = await product_service.update_stock(product_id, stock_update.stock)
    
    if new_stock is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return new_stock

@router.patch("/{product_id}/price")
async def update_price(product_id: int, price_update: PriceUpdate):
    new_price = await product_service.update_price(product_id, price_update.price)
    
    if new_price is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return new_price

@router.patch("/{product_id}/deactivate")
async def deactivate_product(product_id: int):
    product = await product_service.deactivate_product(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return product

@router.patch("/{product_id}/activate")
async def activate_product(product_id: int):
    product = await product_service.activate_product(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    product = await product_service.delete_product(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if product == "ACTIVE":
        raise HTTPException(status_code=409, detail="Produto ainda está ativo. Desative antes de remover definitivamente.")
    
    return {"id": product_id, "message": "Produto removido com sucesso!"}

#@router.delete("/{product_id}/hard")
#async def hard_delete_product(product_id: int):
#    product = await product_service.hard_delete_product(product_id)
#    
#    if product is None:
#        raise HTTPException(status_code=404, detail="Produto não encontrado")
#    
#    return {"id": product_id, "message": "Produto removido com sucesso!"}