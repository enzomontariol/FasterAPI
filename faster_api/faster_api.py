from fastapi import FastAPI
from .router import FasterAPIRouter

class FasterAPI(FasterAPIRouter):
    """FasterAPI is a singleton class that create and run a FastAPI application.
    """
    _instance = None
    
    def __init__(self):
        """Initialization.
        """
        super().__init__()
        self._app = FastAPI()
        self._app.router = self._router

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
    
    async def __call__(self, scope, receive, send):
        """Handle ASGI calls."""
        await self._app(scope, receive, send)