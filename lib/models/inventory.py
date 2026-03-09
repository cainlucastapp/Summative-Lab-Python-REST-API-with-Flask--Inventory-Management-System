# lib/models/inventory.py

class Inventory:
    def __init__(self, id, barcode, product_name, brands, ingredients_text, categories, nutrition_grades, price=0, stock=0):
        self.id = id
        self.barcode = barcode
        self.product_name = product_name
        self.brands = brands
        self.ingredients_text = ingredients_text
        self.categories = categories
        self.nutrition_grades = nutrition_grades
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "product_name": self.product_name,
            "brands": self.brands,
            "ingredients_text": self.ingredients_text,
            "categories": self.categories,
            "nutrition_grades": self.nutrition_grades,
            "price": self.price,
            "stock": self.stock
        }