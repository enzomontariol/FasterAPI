from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Callable, List, Literal, Optional, Any


class FasterAPIRouter:

    def __init__(self) -> None:
        self._router = APIRouter()

    def add_api_route(
        self,
        path: str,
        func: Callable,
        methods=List[Literal["GET", "POST", "PUT", "DELETE", "PATCH"]],
        middleware: Optional[List[Callable[[Request, Callable], Any]]] = None,
        **kwargs
    ) -> Callable:

        if path is None:
            path = self.infer_path(func)

        async def wrapper(request: Request, *args, **kwargs):
            if middleware:
                for mw in middleware:
                    try:
                        response = await mw(request, func)
                    except Exception as e:
                        return JSONResponse(
                            status_code=500,
                            content={
                                "error": "middleware_exceptions",
                                "details": str(e),
                            },
                        )

                    if response:
                        return response
            return await func(*args, **kwargs)

        self._router.add_api_route(path, endpoint=wrapper, methods=methods, **kwargs)
        return func

    def route(self, path: str = None, **kwargs):
        def decorator(func: Callable) -> Callable:
            self.add_api_route(path, func, **kwargs)
            return func

        return decorator

    def get(self, path: str = None, **kwargs):
        return self.route(path, methods=["GET"], **kwargs)

    def post(self, path: str = None, **kwargs):
        return self.route(path, methods=["POST"], **kwargs)

    def put(self, path: str = None, **kwargs):
        return self.route(path, methods=["PUT"], **kwargs)

    def delete(self, path: str = None, **kwargs):
        return self.route(path, methods=["DELETE"], **kwargs)

    def patch(self, path: str = None, **kwargs):
        return self.route(path, methods=["PATCH"], **kwargs)

    def infer_path(self, func: Callable):
        return "/" + func.__name__.replace("_", "-")
