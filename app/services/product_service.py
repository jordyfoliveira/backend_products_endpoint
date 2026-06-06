from app.repositories import product_repository

async def list_products(limit: int = 10, offset: int = 0, is_active: bool | None = None, name: str | None = None, sku: str | None = None):
    return await product_repository.list_products(limit, offset, is_active, name, sku)

async def get_products_inactive():
    return await product_repository.get_products_inactive()

async def get_product_by_id(product_id: int):
    return await product_repository.get_product_by_id(product_id)

async def create_product(product, username: str):
    return await product_repository.create_product(product, username)

async def update_stock(product_id: int, new_stock: int, username: str):
    return await product_repository.update_stock(product_id, new_stock, username)

async def update_price(product_id: int, new_price: float, username: str):
    return await product_repository.update_price(product_id, new_price, username)

async def deactivate_product(product_id: int, username: str):
    return await product_repository.deactivate_product(product_id, username)

async def activate_product(product_id: int, username: str):
    return await product_repository.activate_product(product_id, username)

async def delete_product(product_id: int, username: str):
    return await product_repository.delete_product(product_id, username)

async def hard_delete_product(product_id: int):
    return await product_repository.hard_delete_product(product_id)