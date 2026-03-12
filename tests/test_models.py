# tests/test_models.py

# Requires
import pytest
from models.inventory import Inventory


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


# Inventory instantiation
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


# Inventory to_dict structure
def test_to_dict_returns_correct_structure(sample_item):
    result = sample_item.to_dict()
    expected_keys = {"id", "barcode", "product_name", "brands", "ingredients_text", "categories", "nutrition_grades", "price", "stock"}
    assert set(result.keys()) == expected_keys


# Inventory to_dict values
def test_to_dict_returns_correct_values(sample_item):
    result = sample_item.to_dict()
    assert result["id"] == 1
    assert result["product_name"] == "Organic Almond Milk"
    assert result["price"] == 3.99
    assert result["stock"] == 10


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


# ID must be an int
def test_id_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id="one", barcode="123", product_name="Test", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b")


# Barcode must be a string
def test_barcode_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode=123, product_name="Test", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b")


# Product name must be a non-empty string
def test_product_name_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name=123, brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b")


# Product name cannot be empty
def test_product_name_empty_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b")


# Product name cannot be whitespace
def test_product_name_whitespace_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="   ", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b")


# Brands must be a string
def test_brands_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="Test", brands=123,
                  ingredients_text="None", categories="Cat", nutrition_grades="b")



# Price must be a number
def test_price_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="Test", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b",
                  price="free")


# Price cannot be negative
def test_price_negative_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="Test", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b",
                  price=-1.99)


# Stock must be an int
def test_stock_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="Test", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b",
                  stock="ten")


# Stock cannot be negative
def test_stock_negative_raises_value_error():
    with pytest.raises(ValueError):
        Inventory(id=1, barcode="123", product_name="Test", brands="Brand",
                  ingredients_text="None", categories="Cat", nutrition_grades="b",
                  stock=-1)