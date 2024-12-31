# Documentation 

## Initialization 

A FasterAPI app can be instanciated in two lines : 

```python
from faster_api import FasterAPI

app = FasterAPI()
```
It accepts an optional parameter ```logging_level``` that defines the verbosity level of the app. 

## Adding routes 
Adding a route is as simple as FastAPI's process. 
For example, to create a ```GET``` ```/add``` endpoint that takes two numbers as parameters : 
```python
# Function to add 2 numbers
@app.get("/add")
def add_numbers(a: int, b: int):
    """
    Endpoint pour additionner deux nombres.
    """
    result = a + b
    return {"a": a, "b": b, "sum": result}
```
Supported methods are ```GET```, ```POST```, ```PUT```, ```DELETE``` and ```PATCH```

The only parameter for decorator is ```path```, which indicates the path to be used by the router. It is optional and will be infered from the function name if left blank.  

## Starting the server 

Our goal was to create a functional [ASGI app](https://asgi.readthedocs.io/en/latest/), such that it could easily be integrated with widely used packages like uvicorn. 

As such, to start the app is as easy as : 

```
uvicorn.run(app, port=8000)
```

