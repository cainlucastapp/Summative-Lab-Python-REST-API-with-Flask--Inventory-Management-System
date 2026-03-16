# src/controllers/inventory_controller.py


# Requires
from flask import jsonify, request
from src.providers.inventory_provider import (
    all_items, one_item, add_item, update_item, remove_item,
    search_items, lookup_from_api, import_from_api
)


# Get all items
def get_all():
    return jsonify(all_items()), 200


# Get single item
def get_one(id):
    item = one_item(id)
    return jsonify(item) if item else (jsonify({"error": "Item not found"}), 404)


# Create item
def create():
    data = request.get_json()
    try:
        item = add_item(data)
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(item), 201


# Update item
def update(id):
    data = request.get_json()
    try:
        item = update_item(id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(item) if item else (jsonify({"error": "Item not found"}), 404)


# Delete item
def delete(id):
    removed = remove_item(id)
    return jsonify({"message": f"Item {id} deleted"}) if removed else (jsonify({"error": "Item not found"}), 404)


# Search inventory
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    return jsonify(search_items(query)), 200


# Lookup product by barcode or name
def lookup_product():
    barcode = request.args.get('barcode')
    name = request.args.get('name')
    if not barcode and not name:
        return jsonify({"error": "Query parameter 'barcode' or 'name' is required"}), 400
    product, code = lookup_from_api(barcode=barcode, name=name)
    if code == "timeout":
        return jsonify({"error": "OpenFoodFacts request timed out, please try again"}), 504
    if not product:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
    return jsonify(product), 200


# Import product from OpenFoodFacts
def import_product():
    body = request.get_json(silent=True) or {}
    barcode = body.get('barcode')
    name = body.get('name')
    if not barcode and not name:
        return jsonify({"error": "Request body must include 'barcode' or 'name'"}), 400
    try:
        item, code = import_from_api(
            barcode=barcode,
            name=name,
            price=body.get("price", 0),
            stock=body.get("stock", 0)
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if code == "timeout":
        return jsonify({"error": "OpenFoodFacts request timed out, please try again"}), 504
    if not item:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
    return jsonify(item), 201