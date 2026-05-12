from datetime import datetime
from app.db.connection import get_db_connection as get_conn
from app.utils.formatters import format_product_id
from app.schemas import product as product_schema
from psycopg.types.json import Jsonb

columns = ["id", "sku", "name", "description", "price", "stock", "is_active", "created_at"]

async def log_action(cur, action: str, entity: str, entity_id: int, details: Jsonb):
    await cur.execute(
        """
        INSERT INTO audit_logs (action, entity, entity_id, details)
        VALUES (%s, %s, %s, %s);
        """,
        (action, entity, entity_id, details)
    )
    
async def generate_product_id(cur):
    ano_atual = datetime.now().year
    first_id = ano_atual * 10000
    last_id = ano_atual * 10000 + 9999
    await cur.execute(
        """
        SELECT MAX(id)
        FROM products
        WHERE id BETWEEN %s AND %s;
        """,
        (first_id, last_id)
    )
    row = await cur.fetchone()
    last_product_id = row[0]
    
    if last_product_id is None:
        return first_id
    
    return last_product_id + 1

async def list_products():
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, sku, name, description, price, stock, is_active, created_at
                FROM products
                ORDER BY id;
                """
                )
            rows = await cur.fetchall()
            products = []
            
            for row in rows:
                product = dict(zip(columns, row))
                product["display_id"] = format_product_id(product["id"])
                products.append(product)
            
            return products
            #return [dict(zip(columns, row)) for row in rows]
        
async def get_product_by_id(product_id: int):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, sku, name, description, price, stock, is_active, created_at
                FROM products
                WHERE id = %s;
                """,
                (product_id,)
            )
            row = await cur.fetchone()
            
            if row is None:
                return None

            product = dict(zip(columns, row))
            product["display_id"] = format_product_id(product["id"])
            
            return product
            # return dict(zip(columns, row)) if row else None
        
        
async def create_product(product: product_schema.ProductCreate):
    data = {"sku": product.sku, "name": product.name, "description": product.description, "price": product.price, "stock": product.stock}
    
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            product_id = await generate_product_id(cur)
            await cur.execute(
                """
                INSERT INTO products (id, sku, name, description, price, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (product_id, product.sku, product.name, product.description, product.price, product.stock)
            )
            row = await cur.fetchone()
            product_id = row[0]
            await log_action(cur, "Insert", "products", product_id, Jsonb(data))
            
        return {"id": product_id, "display_id": format_product_id(product_id), "message": "Produto criado com sucesso!"}
        #return product_id
        
async def update_stock(product_id: int, new_stock: int):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                UPDATE products
                SET stock = %s
                WHERE id = %s
                RETURNING id, stock;
                """,
                (new_stock, product_id)
            )
            row = await cur.fetchone()
            
            if row is not None:
                await log_action(cur, "Stock Update", "products", row[0], Jsonb({"stock": new_stock}))
                
        return None if row is None else {"id": row[0], "display_id": format_product_id(row[0]), "stock": row[1], "message": "Stock atualizado com sucesso!"}
        
async def update_price(product_id: int, new_price: float):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                UPDATE products
                SET price = %s
                WHERE id = %s
                RETURNING id, price;
                """,
                (new_price, product_id)
            )
            row = await cur.fetchone()
            
            if row is not None:
                await log_action(cur, "Price Update", "products", row[0], Jsonb({"price": new_price}))
                
        return None if row is None else {"id": row[0], "display_id": format_product_id(row[0]), "price": row[1], "message": "Preço atualizado com sucesso!"}

async def deactivate_product(product_id: int):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
            """
            UPDATE products
            SET is_active = FALSE
            WHERE id = %s
            RETURNING id;
            """,
            (product_id,)
            )
            row = await cur.fetchone()
            
            if row is not None:
                await log_action(cur, "Deactivate", "products", row[0], Jsonb({"is_active": False}))
        
    return None if row is None else {"id": row[0], "display_id": format_product_id(row[0]), "message": "Produto desactivado com sucesso!"}

async def activate_product(product_id: int):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
            """
            UPDATE products
            SET is_active = TRUE
            WHERE id = %s
            RETURNING id;
            """,
            (product_id,)
            )
            row = await cur.fetchone()
            
            if row is not None:
                await log_action(cur, "Activate", "products", row[0], Jsonb({"is_active": True}))
        
    return None if row is None else {"id": row[0], "display_id": format_product_id(row[0]), "message": "Produto reativado com sucesso!"}

async def get_products_inactive():
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
            """
            SELECT id, sku, name, description, price, stock, is_active, created_at
            FROM products
            WHERE is_active = FALSE;
            """,
            )
            rows = await cur.fetchall()
            products_inactive = []
            
            for row in rows:
                product = dict(zip(columns, row))
                product["display_id"] = format_product_id(product["id"])
                products_inactive.append(product)
                
    return products_inactive  

async def delete_product(product_id: int):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
            """
            SELECT is_active
            FROM products
            WHERE id = %s;
            """,
            (product_id,)
            )
            row = await cur.fetchone()
            
            if row is None:
                return None
            
            is_active = row[0]
            
            if is_active:
                return "ACTIVE"
            
            await cur.execute(
            """
            DELETE FROM products
            WHERE id = %s
            returning id;
            """,
            (product_id,)
            )
            
            deleted_row = await cur.fetchone()
            
            if deleted_row is None:
                return None
            
            deleted_product = deleted_row[0]
            
            await log_action(cur, "Delete", "products", deleted_product, Jsonb({}))
            
        return {"id": product_id, "display_id": format_product_id(product_id), "message": "Produto removido com sucesso!"}
            

async def hard_delete_product(product_id: int):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
            """
            DELETE FROM products
            WHERE id = %s
            RETURNING id;
            """,
            (product_id,)
            )
            row = await cur.fetchone()
            
            if row is not None:
                await log_action(cur, "Delete", "products", row[0], Jsonb({}))
                
    return None if row is None else {"id": row[0], "display_id": format_product_id(row[0]), "message": "Produto removido com sucesso!"}

