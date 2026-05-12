def format_product_id(product_id: int) -> str:
    product_id = str(product_id)
    return f"{product_id[:4]}-{product_id[4:]}"