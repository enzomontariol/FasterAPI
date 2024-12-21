from fastapi import APIRouter
from typing import Callable, List, Literal


class FasterAPIRouter:

    def __init__(self) -> None:
        self._router = APIRouter()

    def add_api_route(
        self,
        path: str,
        func: Callable,
        methods=List[Literal["GET", "POST", "PUT", "DELETE", "PATCH"]],
        **kwargs
    ) -> Callable:

        if path is None:
            path = self.infer_path(func)

        self._router.add_api_route(path, endpoint=func, methods=methods, **kwargs)
        return func

    def get(self, path: str = None, **kwargs):
        def decorator(func: Callable) -> Callable:
            self.add_api_route(path, func, methods=["GET"], **kwargs)
            return func

        return decorator

    def post(self, path: str = None, **kwargs):
        def decorator(func: Callable) -> Callable:
            self.add_api_route(path, func, methods=["POST"], **kwargs)
            return func

        return decorator

    def infer_path(self, func: Callable):
        return "/" + func.__name__.replace("_", "-")