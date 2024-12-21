from faster_api import FasterAPI
from dataclasses import dataclass

app = FasterAPI()


@app.get()
def test():
    return {"test": "test"}


@dataclass
class Stock:
    name: str
    price: float


@app.post()
def test_stock(stock: Stock):
    """
    This is a test endpoint 2
    """
    print(stock)
    return {"test": "test2"}


app.run()
