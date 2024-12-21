from fastapi import FastAPI, Response
from .router import FasterAPIRouter
import uvicorn


class FasterAPI(FasterAPIRouter):
    _instance = None
    
    def __init__(self):
        super().__init__()
        self._app = FastAPI()
        self._routers = [self._router]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def run(self): 
        self._app.include_router(self._router)
        uvicorn.run(self._app)