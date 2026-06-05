import asyncio
import json
import httpx

NEW_API = "http://localhost:8001/products"
JSON_FILE = "old_products.json"

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb3JkeSIsInJvbGUiOiJBRE1JTiIsImV4cCI6MTc4MDYzMjc4Mn0.YHb-MuN78qhVIsDxBjujIm0rONo-y72BygWZN7XlhyQ"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}


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

            response = await client.post(
                NEW_API,
                json=payload,
                headers=headers
            )

            if response.status_code == 409:
                print("SKU duplicado:", payload["sku"])
                continue

            print(response.status_code, response.text)
            response.raise_for_status()

            print("Importado:", response.json())


if __name__ == "__main__":
    asyncio.run(main())