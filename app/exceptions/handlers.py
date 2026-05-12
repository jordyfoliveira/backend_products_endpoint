from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import ProductNotFoundError, ProductActiveError, DuplicateSKUError

async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Produto não encontrado"}
    )

async def product_active_handler(request: Request, exc: ProductActiveError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Produto ainda está ativo. Desative antes de remover definitivamente."}
    )
    
async def duplicate_sku_handler(request: Request, exc: DuplicateSKUError):
    return JSONResponse(
        status_code=409,
        content={"detail": "SKU já existente."}
    )