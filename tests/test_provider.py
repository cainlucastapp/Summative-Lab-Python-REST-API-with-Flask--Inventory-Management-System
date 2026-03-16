# tests/test_provider.py

# Requires
import pytest
from src.providers.inventory_provider import (
    all_items, one_item, add_item, update_item, remove_item,
    search_items, normalize_field
)
import src.providers.inventory_provider as provider
from src.models.inventory import Inventory


#Fixtures
@pytest.fixture(autouse=True)
def reset_inventory():
    provider.inventory = [
        Inventory(id=1, barcode="012345678905", product_name="Organic Almond Milk", brands="Silk",
                  ingredients_text="Filtered water, almonds, cane sugar", categories="Plant-based milks",
                  nutrition_grades="a", price=3.99, stock=10),
        Inventory(id=2, barcode="049000028911", product_name="Coca-Cola", brands="Coca-Cola",
                  ingredients_text="Carbonated water, high fructose corn syrup",
                  categories="Sodas", nutrition_grades="e", price=1.99, stock=50),
        Inventory(id=3, barcode="016000275607", product_name="Cheerios", brands="General Mills",
                  ingredients_text="Whole grain oats, modified corn starch, sugar, salt",
                  categories="Breakfast Cereals", nutrition_grades="b", price=4.49, stock=30),
    ]


# all_items returns list of dicts with correct count
def test_all_items():
    result = all_items()
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], dict)


# all_items returns empty list when inventory is empty
def test_all_items_empty():
    provider.inventory = []
    assert all_items() == []


# one_item returns correct item
def test_one_item_returns_item():
    result = one_item(1)
    assert result['product_name'] == "Organic Almond Milk"


# one_item returns None for missing id
def test_one_item_not_found():
    assert one_item(999) is None


# add_item adds item and returns dict
def test_add_item():
    data = {
        "barcode": "111111111111",
        "product_name": "Test Product",
        "brands": "Test Brand",
        "ingredients_text": "Water, sugar",
        "categories": "Test Category",
        "nutrition_grades": "b",
        "price": 2.99,
        "stock": 15
    }
    result = add_item(data)
    assert result['product_name'] == "Test Product"
    assert len(provider.inventory) == 4


# add_item raises KeyError for missing product_name
def test_add_item_missing_product_name():
    with pytest.raises(KeyError):
        add_item({"price": 1.99, "stock": 5})


# add_item raises ValueError for invalid price
def test_add_item_invalid_price():
    with pytest.raises(ValueError):
        add_item({"product_name": "Test", "price": -1, "stock": 5})


# update_item updates and returns dict
def test_update_item():
    result = update_item(1, {"price": 9.99, "stock": 5})
    assert result['price'] == 9.99
    assert result['stock'] == 5


# update_item returns None for missing id
def test_update_item_not_found():
    assert update_item(999, {"price": 9.99}) is None


# remove_item removes item and returns True
def test_remove_item():
    result = remove_item(1)
    assert result is True
    assert len(provider.inventory) == 2


# remove_item returns False for missing id
def test_remove_item_not_found():
    assert remove_item(999) is False


# search_items returns matching results
def test_search_items():
    results = search_items("coca")
    assert len(results) == 1
    assert results[0]['product_name'] == "Coca-Cola"


# search_items returns empty list for no match
def test_search_items_no_match():
    assert search_items("xyz") == []


# normalize_field converts list to string
def test_normalize_field_list():
    assert normalize_field(["General Mills"]) == "General Mills"


# normalize_field returns default for invalid type
def test_normalize_field_invalid():
    assert normalize_field(123) == ""