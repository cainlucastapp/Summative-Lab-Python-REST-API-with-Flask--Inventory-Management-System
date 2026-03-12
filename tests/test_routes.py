# tests/test_routes.py


# Requires
import pytest
from unittest.mock import patch
from app import app
import controllers.inventory_controller as ctrl


#Fixtures
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


#Fixtures
@pytest.fixture(autouse=True)
def reset_inventory():
    ctrl.inventory = [
        ctrl.Inventory(id=1, barcode="012345678905", product_name="Organic Almond Milk", brands="Silk",
                       ingredients_text="Filtered water, almonds, cane sugar", categories="Plant-based milks",
                       nutrition_grades="a", price=3.99, stock=10),
        ctrl.Inventory(id=2, barcode="049000028911", product_name="Coca-Cola", brands="Coca-Cola",
                       ingredients_text="Carbonated water, high fructose corn syrup",
                       categories="Sodas", nutrition_grades="e", price=1.99, stock=50),
        ctrl.Inventory(id=3, barcode="016000275607", product_name="Cheerios", brands="General Mills",
                       ingredients_text="Whole grain oats, modified corn starch, sugar, salt",
                       categories="Breakfast Cereals", nutrition_grades="b", price=4.49, stock=30),
    ]


# GET /inventory returns 200 and all items
def test_get_all(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert len(response.get_json()) == 3


# GET /inventory/<id> returns 200 and correct item
def test_get_one(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.get_json()['product_name'] == "Organic Almond Milk"


# GET /inventory/<id> returns 404 for missing item
def test_get_one_not_found(client):
    response = client.get('/inventory/999')
    assert response.status_code == 404


# POST /inventory creates item and returns 201
def test_create(client):
    response = client.post('/inventory', json={
        "barcode": "111111111111",
        "product_name": "Test Product",
        "brands": "Test Brand",
        "ingredients_text": "Water, sugar",
        "categories": "Test Category",
        "nutrition_grades": "b",
        "price": 2.99,
        "stock": 15
    })
    assert response.status_code == 201
    assert response.get_json()['product_name'] == "Test Product"


# POST /inventory returns 400 for missing product_name
def test_create_missing_product_name(client):
    response = client.post('/inventory', json={"price": 1.99, "stock": 5})
    assert response.status_code == 400


# PATCH /inventory/<id> updates item and returns 200
def test_update(client):
    response = client.patch('/inventory/1', json={"price": 9.99, "stock": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data['price'] == 9.99
    assert data['stock'] == 5


# PATCH /inventory/<id> returns 404 for missing item
def test_update_not_found(client):
    response = client.patch('/inventory/999', json={"price": 9.99})
    assert response.status_code == 404


# DELETE /inventory/<id> removes item and returns 200
def test_delete(client):
    response = client.delete('/inventory/1')
    assert response.status_code == 200
    assert len(ctrl.inventory) == 2


# DELETE /inventory/<id> returns 404 for missing item
def test_delete_not_found(client):
    response = client.delete('/inventory/999')
    assert response.status_code == 404


# GET /inventory/search returns matching items
def test_search(client):
    response = client.get('/inventory/search?q=coca')
    assert response.status_code == 200
    results = response.get_json()
    assert len(results) == 1
    assert results[0]['product_name'] == "Coca-Cola"


# GET /inventory/search returns 400 with no query
def test_search_no_query(client):
    response = client.get('/inventory/search')
    assert response.status_code == 400


# GET /inventory/lookup returns product by barcode
def test_lookup_barcode(client):
    mock_product = {
        "product_name": "Coca-Cola",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water",
        "categories": "Sodas",
        "nutrition_grades": "e"
    }
    with patch('controllers.inventory_controller.fetch_from_api', return_value=(mock_product, "049000028911")):
        response = client.get('/inventory/lookup?barcode=049000028911')
        assert response.status_code == 200
        assert response.get_json()['product_name'] == "Coca-Cola"


# GET /inventory/lookup returns 404 for unknown barcode
def test_lookup_barcode_not_found(client):
    with patch('controllers.inventory_controller.fetch_from_api', return_value=(None, None)):
        response = client.get('/inventory/lookup?barcode=000000000000')
        assert response.status_code == 404


# GET /inventory/lookup returns product by name
def test_lookup_name(client):
    mock_product = {
        "product_name": "Cheerios",
        "brands": ["General Mills"],
        "ingredients_text": "Whole grain oats",
        "categories": "Breakfast Cereals",
        "nutrition_grades": "b"
    }
    with patch('controllers.inventory_controller.fetch_from_api', return_value=(mock_product, "016000275607")):
        response = client.get('/inventory/lookup?name=cheerios')
        assert response.status_code == 200
        assert response.get_json()['product_name'] == "Cheerios"


# GET /inventory/lookup returns 504 on timeout
def test_lookup_name_timeout(client):
    with patch('controllers.inventory_controller.fetch_from_api', return_value=(None, "timeout")):
        response = client.get('/inventory/lookup?name=cheerios')
        assert response.status_code == 504


# GET /inventory/lookup returns 400 with no query params
def test_lookup_no_params(client):
    response = client.get('/inventory/lookup')
    assert response.status_code == 400


# POST /inventory/import adds product from API and returns 201
def test_import_product(client):
    mock_product = {
        "product_name": "Cheerios",
        "brands": ["General Mills"],
        "ingredients_text": "Whole grain oats",
        "categories": "Breakfast Cereals",
        "nutrition_grades": "b"
    }
    with patch('controllers.inventory_controller.fetch_from_api', return_value=(mock_product, "016000275607")):
        response = client.post('/inventory/import', json={"name": "cheerios", "price": 4.49, "stock": 30})
        assert response.status_code == 201
        assert response.get_json()['product_name'] == "Cheerios"


# POST /inventory/import returns 400 with no name or barcode
def test_import_missing_body(client):
    response = client.post('/inventory/import', json={})
    assert response.status_code == 400


# GET /inventory returns empty list when inventory is empty
def test_get_all_empty(client):
    ctrl.inventory = []
    response = client.get('/inventory')
    assert response.status_code == 200
    assert response.get_json() == []


# DELETE /inventory/<id> returns 404 when inventory is empty
def test_delete_empty_inventory(client):
    ctrl.inventory = []
    response = client.delete('/inventory/1')
    assert response.status_code == 404