from faster_api import FasterAPI
from dataclasses import dataclass
from fastapi.testclient import TestClient
from fastapi import Request

import unittest

app = FasterAPI()


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API"}


# Example with GET
@app.get()
def test():
    return {"test": "test"}


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


def check_access_token(request, func):
    if request.headers.get("Authorization", "") != "123":
        raise Exception("Access denied")


@app.get("/restricted-access", middleware=[check_access_token])
def restricted_access(request: Request):
    return {"message": "Successfull access to restricted content"}


# === Unit testings ===


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        """
        Test de la route racine.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Bienvenue sur l'API"})

    def test_add_numbers(self):
        """
        Test de l'addition de deux nombres.
        """
        response = self.client.get("/add?a=5&b=7")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"a": 5, "b": 7, "sum": 12})

    def test_stock(self):
        """
        Test de la route test_stock.
        """
        payload = {"name": "Apple", "price": 150.0}
        response = self.client.post("/test-stock", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "Apple", "price": 150.0})

    def test_restricted_access(self):
        """
        Test de la route restricted-access.
        """
        response = self.client.get(
            "/restricted-access", headers={"Authorization": "123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": "Successfull access to restricted content"}
        )


if __name__ == "__main__":
    unittest.main()
