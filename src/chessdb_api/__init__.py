"""Collection of functions initializing FastAPI application.

This is the main entry point, of creating the FastAPI application. The
application gets created, then gets extensions initialized and routes
registered.
"""

from fastapi import FastAPI

from chessdb_api.core import version
from chessdb_api.core.db import DB
from chessdb_api.routers import positions


def create_app() -> FastAPI:
    """Main entry point for creating application

    Returns:
        FastAPI: An instance of fastAPI application.
    """
    app: FastAPI = FastAPI(title="ChessDB API", version=version.__version__)
    _initalize_extensions(app=app)
    return _register_routes(app=app)


def _register_routes(app: FastAPI) -> FastAPI:
    """Registers routes on the application

    Args:
        app (FastAPI): FastAPI application

    Returns:
        FastAPI: FastAPI application with routes registered.
    """
    app.include_router(positions.router,
                       prefix="/positions",
                       tags=["Positions"])
    return app


def _initalize_extensions(app: FastAPI):
    """Initializes extensions such as database

    Args:
        app (FastAPI): FastAPI application
    """
    DB.init_app(app=app)
