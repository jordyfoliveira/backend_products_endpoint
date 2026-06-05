import asyncio
import json
import httpx

NEW_API = "http://localhost:8001/products"
JSON_FILE = "old_products.json"


async def main():
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        old_products = json.load(file)

    async with httpx.AsyncClient(timeout=60.0) as client:
        for product in old_products:
            payload = {
                "sku": product["sku"],
                "name": product["name"],
                "description": product.get("description") or "",
                "price": float(product["price"]),
                "stock": int(product["stock"]),
            }

            response = await client.post(NEW_API, json=payload)

            if response.status_code == 409:
                print("SKU duplicado:", payload["sku"])
                continue

            response.raise_for_status()
            print("Importado:", response.json())


if __name__ == "__main__":
    asyncio.run(main())