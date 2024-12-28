from fastapi import FastAPI
from .router import FasterAPIRouter
from .config import FasterAPIConfig
import uvicorn


class FasterAPI(FasterAPIRouter):
    """FasterAPI is a singleton class that create and run a FastAPI application.
    """
    _instance = None
    
    def __init__(self):
        """Initialization.
        """
        super().__init__()
        self._app = FastAPI()
        self._routers = [self._router]
        self._config = FasterAPIConfig()

    def __new__(cls):
        """Create and return a new instance of the class.

        This method ensures that only one instance of the class is created (singleton pattern).
        If an instance already exists, it returns the existing instance.

        Returns:
            FasterAPI: The single instance of the FasterAPI class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def run(self):
        """Method to run the service.
        """
        self._app.include_router(self._router)
        uvicorn.run(self._app, host=self._config._host, port=self._config._port)