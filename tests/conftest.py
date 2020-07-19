"""Example Google style docstrings.

"""
import pathlib
import subprocess

import pytest

import chessdb_api
from fastapi import testclient


@pytest.fixture
def app():
    """app.
    """
    return chessdb_api.create_app()


@pytest.fixture
def client(app):
    """client.

    Args:
        app:
    """
    cwd = pathlib.Path(__file__).parent.parent
    subprocess.check_call(["alembic", "upgrade", "head"], cwd=cwd)
    with testclient.TestClient(app, "http://localhost:12001") as test_client:
        yield test_client
