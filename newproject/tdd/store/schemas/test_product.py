from uuid import UUID
from product import ProductIn


def test_schemas_validated():
    data =  {"name": "Iphone 14 pro Max", "quantity": 10, "price": 8.500, "status": True}
    product = ProductIn(**data)
    # product = ProductIn(name="Iphone 14 pro Max", quantity=10, price=8.500, status=True)
    assert product.name == "Iphone 14 pro Max"
    assert isinstance(product.id, UUID)