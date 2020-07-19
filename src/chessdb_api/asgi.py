"""Asyncronus server gateway interface.

This is for running in production.
"""
from chessdb_api import create_app

app = create_app()
