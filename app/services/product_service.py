from app.repositories import product_repository

async def list_products():
    return await product_repository.list_products()

async def get_products_inactive():
    return await product_repository.get_products_inactive()

async def get_product_by_id(product_id: int):
    return await product_repository.get_product_by_id(product_id)

async def create_product(product):
    return await product_repository.create_product(product)

async def update_stock(product_id: int, new_stock: int):
    return await product_repository.update_stock(product_id, new_stock)

async def update_price(product_id: int, new_price: float):
    return await product_repository.update_price(product_id, new_price)

async def deactivate_product(product_id: int):
    return await product_repository.deactivate_product(product_id)

async def activate_product(product_id: int):
    return await product_repository.activate_product(product_id)

async def delete_product(product_id: int):
    return await product_repository.delete_product(product_id)

async def hard_delete_product(product_id: int):
    return await product_repository.hard_delete_product(product_id)