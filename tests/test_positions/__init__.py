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


def mock_position(street_position: str = None, zip_number: int = None):
    if street_position is None:
        street_position = f"{utils.random_string(length=10)} {utils.random_string(length=8)} 101"

    if zip_number is None:
        zip_number = random.randint(1000, 10000)

    return dict(street_position=street_position, zip_number=zip_number)


def no_state_change(data: Dict[str, Any],
                    position: Dict[str, Any],
                    identifier: pydantic.UUID4 = None) -> None:
    assert position["street_position"] == data["street_position"]
    assert position["zip_number"] == data["zip_number"]
    if identifier:
        assert identifier == data["identifier"]
