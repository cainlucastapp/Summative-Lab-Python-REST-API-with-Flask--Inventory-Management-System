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

    # ID
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("id must be an int")
        self._id = value


    # Barcode
    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value):
        if not isinstance(value, str):
            raise ValueError("barcode must be a string")
        self._barcode = value


    # Product Name
    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("product_name must be a non-empty string")
        self._product_name = value


    # Brands
    @property
    def brands(self):
        return self._brands

    @brands.setter
    def brands(self, value):
        if not isinstance(value, str):
            raise ValueError("brands must be a string")
        self._brands = value


    # Ingredients Text
    @property
    def ingredients_text(self):
        return self._ingredients_text

    @ingredients_text.setter
    def ingredients_text(self, value):
        if not isinstance(value, str):
            raise ValueError("ingredients_text must be a string")
        self._ingredients_text = value


    # Categories
    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        if not isinstance(value, str):
            raise ValueError("categories must be a string")
        self._categories = value


    # Nutrition Grades
    @property
    def nutrition_grades(self):
        return self._nutrition_grades

    @nutrition_grades.setter
    def nutrition_grades(self, value):
        if not isinstance(value, str):
            raise ValueError("nutrition_grades must be a string")
        self._nutrition_grades = value


    # Price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("price must be a non-negative number")
        self._price = value


    # Stock
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("stock must be a non-negative int")
        self._stock = value


    # Convert to dictionary for JSON serialization
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