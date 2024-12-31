from faster_api import FasterAPI
from dataclasses import dataclass
from fastapi.testclient import TestClient

import unittest

app = FasterAPI()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API"}

# Example with GET
@app.get()
def test():
    return {"test": "test"}

# Example of dataclass 
@dataclass
class Stock:
    name: str
    price: float

# Example with POST
@app.post("/test-stock")
def stock(stock: Stock):
    """
    Endpoint pour tester une classe Stock.
    """
    return {"name": stock.name, "price": stock.price}

# Function to add 2 numbers
@app.get("/add")
def add_numbers(a: int, b: int):
    """
    Endpoint pour additionner deux nombres.
    """
    result = a + b
    return {"a": a, "b": b, "sum": result}

client = TestClient(app)

# === Unit testings ===

class TestApp(unittest.TestCase):
    
    def test_root(self):
        """
        Test de la route racine.
        """
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Bienvenue sur l'API"}


    def test_add_numbers(self):
        """
        Test de l'addition de deux nombres.
        """
        response = client.get("/add?a=5&b=7")
        assert response.status_code == 200
        assert response.json() == {"a": 5, "b": 7, "sum": 12}

    def test_stock(self):
        """
        Test de la route test_stock.
        """
        payload = {"name": "Apple", "price": 150.0}
        response = client.post("/test-stock", json=payload)
        assert response.status_code == 200
        assert response.json() == {"name": "Apple", "price": 150.0}

if __name__ == "__main__":
    unittest.main()