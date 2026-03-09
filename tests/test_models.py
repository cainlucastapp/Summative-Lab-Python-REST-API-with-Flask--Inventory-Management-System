# tests/test_models.py

# Requires
import pytest
from lib.models.inventory import Inventory


#Fixtures
@pytest.fixture
def sample_item():
    return Inventory(
        id=1,
        barcode="012345678905",
        product_name="Organic Almond Milk",
        brands="Silk",
        ingredients_text="Filtered water, almonds, cane sugar",
        categories="Plant-based milks",
        nutrition_grades="a",
        price=3.99,
        stock=10
    )


# Inventory method
def test_inventory_instantiation(sample_item):
    assert sample_item.id == 1
    assert sample_item.barcode == "012345678905"
    assert sample_item.product_name == "Organic Almond Milk"
    assert sample_item.brands == "Silk"
    assert sample_item.ingredients_text == "Filtered water, almonds, cane sugar"
    assert sample_item.categories == "Plant-based milks"
    assert sample_item.nutrition_grades == "a"
    assert sample_item.price == 3.99
    assert sample_item.stock == 10


# Price defaults to zero
def test_price_defaults_to_zero():
    item = Inventory(id=1, barcode="123", product_name="Test", brands="Brand",
                     ingredients_text="None", categories="Cat", nutrition_grades="b")
    assert item.price == 0


# Stock defaults to zero
def test_stock_defaults_to_zero():
    item = Inventory(id=1, barcode="123", product_name="Test", brands="Brand",
                     ingredients_text="None", categories="Cat", nutrition_grades="b")
    assert item.stock == 0


# Missing required fields raises TypeError
def test_missing_required_fields_raises_type_error():
    with pytest.raises(TypeError):
        Inventory()