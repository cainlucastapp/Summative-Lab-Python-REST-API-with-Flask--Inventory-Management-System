# app.py


# Requires
from flask import Flask, render_template
from src.providers.inventory_provider import get_all, get_one, create, update, delete, search, lookup_product, import_product


# Initialize app
app = Flask(__name__, template_folder='../client/templates', static_folder='../client/static')


# Config
app.config['API_BARCODE_URL'] = "https://world.openfoodfacts.org/api/v2"
app.config['API_SEARCH_URL'] = "https://search.openfoodfacts.org/search"


# GET / - Serve index
@app.route('/')
def index():
    return render_template('index.html')

# GET /inventory - Get all items
@app.route('/inventory', methods=['GET'])
def get_all_items():
    return get_all()


# GET /inventory/<id> - Get single item
@app.route('/inventory/<int:id>', methods=['GET'])
def get_one_item(id):
    return get_one(id)


# POST /inventory - Create item
@app.route('/inventory', methods=['POST'])
def create_item():
    return create()


# PATCH /inventory/<id> - Update item
@app.route('/inventory/<int:id>', methods=['PATCH'])
def update_item(id):
    return update(id)


# DELETE /inventory/<id> - Remove item
@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_item(id):
    return delete(id)


# GET /inventory/search - Search inventory
@app.route('/inventory/search', methods=['GET'])
def search_inventory():
    return search()


# GET /inventory/lookup - Lookup product by barcode or name
@app.route('/inventory/lookup', methods=['GET'])
def lookup_from_api():
    return lookup_product()


# POST /inventory/import - Import product from OpenFoodFacts (by product name or barcode)
@app.route('/inventory/import', methods=['POST'])
def import_from_api():
    return import_product()


if __name__ == "__main__":
    app.run(debug=True)