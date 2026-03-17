# Food Inventory Manager

A RESTful API built with Flask for managing a food inventory, with an HTML/JavaScript frontend and OpenFoodFacts API integration.

## Setup

### Prerequisites
- Python 3.10+
- pipenv

### Installation

```bash
git clone <repo-url>
cd <project-folder>
pipenv install
```

### Running the App

```bash
pipenv run python -m src.app
```

Visit `http://127.0.0.1:5000`

---

## Project Structure

```
src/
  models/          # Inventory class with validation
  providers/       # Data layer and external API logic
  controllers/     # HTTP request/response handling
  app.py           # Flask routes
client/
  templates/       # Jinja2 HTML templates
  static/          # CSS, JS, images
tests/
  test_models.py   # Unit tests for Inventory model
  test_provider.py # Unit tests for provider functions
  test_routes.py   # Integration tests for all routes
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | Get all items |
| GET | `/inventory/<id>` | Get single item |
| POST | `/inventory` | Create item |
| PATCH | `/inventory/<id>` | Update item |
| DELETE | `/inventory/<id>` | Delete item |
| GET | `/inventory/search?q=` | Search inventory |
| GET | `/inventory/lookup?barcode=` | Lookup product by barcode |
| GET | `/inventory/lookup?name=` | Lookup product by name |

---

## External API

Product data is fetched from [OpenFoodFacts](https://world.openfoodfacts.org/).

- Barcode lookup: `https://world.openfoodfacts.org/api/v2/product/{barcode}.json`
- Name search: `https://search.openfoodfacts.org/search`

---

## Testing

```bash
pipenv run pytest
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| flask | Web framework |
| requests | External API calls |
| pytest | Testing |