import random
import string
from typing import Any, Dict, Tuple

import pydantic
import pytest
from requests import exceptions

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
def update_position(client, position: dict, identifier: pydantic.UUID4):
    return client.put(ROUTE + identifier, json=position)


@raise_for_status
def delete_position(client, identifier: pydantic.UUID4):
    return client.delete(ROUTE + identifier)


@raise_for_status
def get_position(client, identifier: pydantic.UUID4):
    return client.get(ROUTE + identifier)


@raise_for_status
def get_positions(client, page: int = 1, page_size: int = 50):
    return client.get(ROUTE, params=dict(page=page, page_size=page_size))


def mock_position(
        fen="rnbqkbnr/pp1ppppp/2p5/8/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"):
    return dict(fen=fen)


def no_state_change(data: Dict[str, Any],
                    position: Dict[str, Any],
                    identifier: pydantic.UUID4 = None) -> None:
    assert position["street_position"] == data["street_position"]
    assert position["zip_number"] == data["zip_number"]
    if identifier:
        assert identifier == data["identifier"]
