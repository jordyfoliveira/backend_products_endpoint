from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    sku: str = Field(..., pattern="^SKU\d{3}$")
    name: str = Field(..., min_length=3)
    description: str = ""
    price: float = Field(..., ge=0.01)
    stock: int = Field(..., gt=0)
    
class StockUpdate(BaseModel):
    stock: int = Field(..., ge=0)
    
class PriceUpdate(BaseModel):
    price: float = Field(..., ge=0.01)
