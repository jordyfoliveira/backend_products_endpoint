from app.utils.formatters import format_product_id

def test_format_product_id():
    assert format_product_id(20260001) == "2026-0001"
    
def test_format_product_id_last():
    assert format_product_id(20269999) == "2026-9999"