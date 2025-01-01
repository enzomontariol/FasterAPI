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

There are two optional parameters for the decorator : 

- ```path```, which indicates the path to be used by the router. It is optional and will be infered from the function name if left blank.  
- ```middleware``` which is a list of middlewares to be used when responding to the request.  

## Using middlewares

Middlewares can be used to perform authentication, compute time to complete a request etc... 
They are functions that are passed to the decorator, that will be ran when a request is made to the endpoint. 
They take in two parameters : 

-  ```request```, a FastAPI Request object that contains all informations about the request, such as headers. 
- ```func``` the function that is decorated. 

If the middleware returns a value or raises an exception, it is sent as the response and the process ends there. 

Example for a simple authentication process : 
```python
def check_access_token(request, func):
    if request.headers.get("Authorization", "") != "123":
        raise Exception("Access denied")

@app.get("/restricted-access", middleware=[check_access_token])
def restricted_access(request: Request):
    return {"message": "Successfull access to restricted content"}
```

## Starting the server 

Our goal was to create a functional [ASGI app](https://asgi.readthedocs.io/en/latest/), such that it could easily be integrated with widely used packages like uvicorn. 

As such, to start the app is as easy as : 

```
uvicorn.run(app, port=8000)
```

