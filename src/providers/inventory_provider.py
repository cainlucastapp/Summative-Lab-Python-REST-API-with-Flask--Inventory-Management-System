# controllers/inventory_controller.py


# Requires
from flask import jsonify, request, current_app
import requests
from src.models.inventory import Inventory


# Seed data
inventory = [
    Inventory(id=1, barcode="012345678905", product_name="Organic Almond Milk", brands="Silk",
              ingredients_text="Filtered water, almonds, cane sugar", categories="Plant-based milks",
              nutrition_grades="a", price=3.99, stock=10),
    Inventory(id=2, barcode="049000028911", product_name="Coca-Cola", brands="Coca-Cola",
              ingredients_text="Carbonated water, high fructose corn syrup, caramel color, phosphoric acid",
              categories="Sodas", nutrition_grades="e", price=1.99, stock=50),
    Inventory(id=3, barcode="016000275607", product_name="Cheerios", brands="General Mills",
              ingredients_text="Whole grain oats, modified corn starch, sugar, salt",
              categories="Breakfast Cereals", nutrition_grades="b", price=4.49, stock=30),
]


# Find item by ID
def find_item(id):
    return next((i for i in inventory if i.id == id), None)


# Get next available ID
def get_next_id():
    return max([i.id for i in inventory]) + 1 if inventory else 1


# Normalize API field that may be a list or string
def normalize_field(value, default=""):
    if isinstance(value, list):
        return ", ".join(value)
    return value if isinstance(value, str) else default


# Get all items
def get_all():
    return jsonify([item.to_dict() for item in inventory]), 200


# Get single item
def get_one(id):
    item = find_item(id)
    return jsonify(item.to_dict()) if item else (jsonify({"error": "Item not found"}), 404)


# Create item
def create():
    data = request.get_json()
    try:
        new_item = Inventory(
            id=get_next_id(),
            barcode=data.get("barcode", ""),
            product_name=data["product_name"],
            brands=data.get("brands", ""),
            ingredients_text=data.get("ingredients_text", ""),
            categories=data.get("categories", ""),
            nutrition_grades=data.get("nutrition_grades", ""),
            price=data.get("price", 0),
            stock=data.get("stock", 0)
        )
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400
    inventory.append(new_item)
    return jsonify(new_item.to_dict()), 201


# Update item
def update(id):
    item = find_item(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    try:
        if "barcode" in data: item.barcode = data["barcode"]
        if "product_name" in data: item.product_name = data["product_name"]
        if "brands" in data: item.brands = data["brands"]
        if "ingredients_text" in data: item.ingredients_text = data["ingredients_text"]
        if "categories" in data: item.categories = data["categories"]
        if "nutrition_grades" in data: item.nutrition_grades = data["nutrition_grades"]
        if "price" in data: item.price = data["price"]
        if "stock" in data: item.stock = data["stock"]
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(item.to_dict()), 200


# Delete item
def delete(id):
    global inventory
    item = find_item(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory = [i for i in inventory if i.id != id]
    return jsonify({"message": f"Item {id} deleted"}), 200


# Search inventory
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    results = [i.to_dict() for i in inventory if
               query in i.product_name.lower() or
               query in i.brands.lower() or
               query in i.categories.lower()]
    return jsonify(results), 200




# Fetch from OpenFoodFacts by barcode or name
def fetch_from_api(barcode=None, name=None):
    base_url = current_app.config['API_BARCODE_URL']
    search_url = current_app.config['API_SEARCH_URL']
    try:
        if barcode:
            response = requests.get(f"{base_url}/product/{barcode}.json", timeout=15)
            data = response.json()
            if data.get("status") != 1:
                return None, None
            return data["product"], barcode
        response = requests.get(search_url, params={
            "q": name,
            "page_size": 1,
            "fields": "code,product_name,brands,ingredients_text,categories,nutrition_grades"
        }, timeout=15)
        data = response.json()
        hits = data.get("hits", [])
        if not hits:
            return None, None
        return hits[0], hits[0].get("code", "")
    except requests.exceptions.Timeout:
        return None, "timeout"
    

# Lookup product by barcode or name
def lookup_product():
    barcode = request.args.get('barcode')
    name = request.args.get('name')
    if not barcode and not name:
        return jsonify({"error": "Query parameter 'barcode' or 'name' is required"}), 400
    product, code = fetch_from_api(barcode=barcode) if barcode else fetch_from_api(name=name)
    if code == "timeout":
        return jsonify({"error": "OpenFoodFacts request timed out, please try again"}), 504
    if not product:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
    return jsonify({
        "barcode": code,
        "product_name": normalize_field(product.get("product_name")),
        "brands": normalize_field(product.get("brands")),
        "ingredients_text": normalize_field(product.get("ingredients_text")),
        "categories": normalize_field(product.get("categories")),
        "nutrition_grades": normalize_field(product.get("nutrition_grades"))
    }), 200


# Import product from OpenFoodFacts (by product name or barcode)
def import_product():
    body = request.get_json(silent=True) or {}
    barcode = body.get('barcode')
    name = body.get('name')
    if not barcode and not name:
        return jsonify({"error": "Request body must include 'barcode' or 'name'"}), 400
    product, code = fetch_from_api(barcode=barcode) if barcode else fetch_from_api(name=name)
    if code == "timeout":
        return jsonify({"error": "OpenFoodFacts request timed out, please try again"}), 504
    if not product:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
    try:
        new_item = Inventory(
            id=get_next_id(),
            barcode=code,
            product_name=normalize_field(product.get("product_name")),
            brands=normalize_field(product.get("brands")),
            ingredients_text=normalize_field(product.get("ingredients_text")),
            categories=normalize_field(product.get("categories")),
            nutrition_grades=normalize_field(product.get("nutrition_grades")),
            price=body.get("price", 0),
            stock=body.get("stock", 0)
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    inventory.append(new_item)
    return jsonify(new_item.to_dict()), 201