# app.py

# Requires
from flask import Flask, render_template

# Initialize app
app = Flask(__name__)

# GET / - Serve index
@app.route('/')
def index():
    return render_template('index.html')

# GET /inventory - Get all items

# GET /inventory/<id> - Get single item

# POST /inventory - Create item

# PATCH /inventory/<id> - Update item

# DELETE /inventory/<id> - Remove item

# GET /inventory/count - Get inventory count

# GET /inventory/search - Search inventory

# GET /inventory/lookup - Lookup product on OpenFoodFacts (by product name or barcode)

# POST /inventory/import - Import product from OpenFoodFacts (by product name or barcode)

if __name__ == "__main__":
    app.run(debug=True)