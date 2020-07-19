from typing import Any
from typing import Dict
from typing import Tuple

import pytest
from requests import exceptions

import pydantic
from tests import utils

ROUTE = "/positions/"


def raise_for_status(func):

    def wrapper(*args, **kwargs) -> Tuple[Dict[str, Any], int]:
        print(f"Called wrapper with function: '{func.__name__}'.")
        print(f"args: '{args}', kwargs '{kwargs}'.")
        response = func(*args, **kwargs)
        print(f"response saved, status code: {response.status_code}")
        response.raise_for_status()
        return response.json(), response.status_code

    return wrapper


@raise_for_status
def create_position(client, position: dict):
    return client.post(ROUTE, json=position)


@raise_for_status
def update_position(client, position: dict, fen: str):
    return client.put(ROUTE + fen, json=position)


@raise_for_status
def delete_position(client, fen: str):
    return client.delete(ROUTE + fen)


@raise_for_status
def get_position(client, fen: str):
    return client.get(ROUTE + fen)


@raise_for_status
def get_positions(client, page: int = 1, page_size: int = 50):
    return client.get(ROUTE, params=dict(page=page, page_size=page_size))


def mock_position():
    return dict(fen=utils.random_string(length=90))


def no_state_change(data: Dict[str, Any],
                    position: Dict[str, Any],
                    fen: str = None) -> None:
    assert position["fen"] == data["fen"]
