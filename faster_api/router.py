from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Callable, List, Literal, Optional, Any
import logging
from functools import wraps


class FasterAPIRouter:

    def __init__(self, logging_level=logging.INFO) -> None:
        """Initialization."""
        self._router = APIRouter()
        self.logger = logging.getLogger("FasterAPIRouter")
        logging.basicConfig(level=logging_level)

    def add_api_route(
        self,
        path: str,
        func: Callable,
        methods=List[Literal["GET", "POST", "PUT", "DELETE", "PATCH"]],
        middleware: Optional[List[Callable[[Request, Callable], Any]]] = None,
        **kwargs,
    ) -> Callable:
        """Adds an API route to the router with optional middleware.

        Args:
            path (str): The path for the API route.
            func (Callable): The endpoint function to be called for the route.
            methods (List[Literal["GET", "POST", "PUT", "DELETE", "PATCH"]]): The HTTP methods allowed for the route.
            middleware (Optional[List[Callable[[Request, Callable], Any]]]): Optional middleware functions to be executed before the endpoint function.
            **kwargs: Additional keyword arguments to be passed to the APIRouter.add_api_route method.

        Returns:
            Callable: The original endpoint function.
        """

        if path is None:
            path = self.infer_path(func)

        self.logger.info(f"Registering path: {path} with methods: {methods}")

        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if middleware:
                for mw in middleware:
                    try:
                        response = mw(request, func)
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
            return func(*args, **kwargs)

        self._router.add_api_route(
            path,
            endpoint=wrapper,
            methods=methods,
            **kwargs,
        )
        return func

    def route(self, path: str = None, **kwargs) -> Callable:
        """A decorator to add an API route to the router.

        Args:
            path (str): The path for the API route.
            **kwargs: Additional keyword arguments to be passed to the add_api_route method.

        Returns:
            Callable: A decorator function that registers the endpoint function as an API route.
        """

        def decorator(func: Callable) -> Callable:
            self.add_api_route(path, func, **kwargs)
            return func

        return decorator

    def get(self, path: str = None, **kwargs) -> Callable:
        """A decorator to add a GET route to the router.

        Args:
            path (str): The path for the GET route.
            **kwargs: Additional keyword arguments to be passed to the add_api_route method.

        Returns:
            Callable: A decorator function that registers the endpoint function as a GET route.
        """
        return self.route(path, methods=["GET"], **kwargs)

    def post(self, path: str = None, **kwargs) -> Callable:
        """
        A decorator to add a POST route to the router.

        Args:
            path (str): The path for the POST route.
            **kwargs: Additional keyword arguments to be passed to the add_api_route method.

        Returns:
            Callable: A decorator function that registers the endpoint function as a POST route.
        """
        return self.route(path, methods=["POST"], **kwargs)

    def put(self, path: str = None, **kwargs) -> Callable:
        """
        A decorator to add a PUT route to the router.

        Args:
            path (str): The path for the PUT route.
            **kwargs: Additional keyword arguments to be passed to the add_api_route method.

        Returns:
            Callable: A decorator function that registers the endpoint function as a PUT route.
        """
        return self.route(path, methods=["PUT"], **kwargs)

    def delete(self, path: str = None, **kwargs) -> Callable:
        """
        A decorator to add a DELETE route to the router.

        Args:
            path (str): The path for the DELETE route.
            **kwargs: Additional keyword arguments to be passed to the add_api_route method.

        Returns:
            Callable: A decorator function that registers the endpoint function as a DELETE route.
        """
        return self.route(path, methods=["DELETE"], **kwargs)

    def patch(self, path: str = None, **kwargs) -> Callable:
        """
        A decorator to add a PATCH route to the router.

        Args:
            path (str): The path for the PATCH route.
            **kwargs: Additional keyword arguments to be passed to the add_api_route method.

        Returns:
            Callable: A decorator function that registers the endpoint function as a PATCH route.
        """
        return self.route(path, methods=["PATCH"], **kwargs)

    def infer_path(self, func: Callable) -> Callable:
        """
        Infers the path for an API route based on the function name.

        Args:
            func (Callable): The endpoint function.

        Returns:
            str: The inferred path for the API route.
        """
        return "/" + func.__name__.replace("_", "-")
