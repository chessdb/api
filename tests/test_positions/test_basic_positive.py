"""Basic positive tests (happy paths).

This module executes API calls with valid required parameters.

Validation checks:
    Validate status code: All requests should return 2XX HTTP status codes.
    Validate payload: Response is a well-formed JSON object.
    Validate state: GET requests should not change state.
    Validate headers: Verifies if headers are the same as expected.
"""

import pytest
from requests import exceptions

import pydantic
from tests import test_positions
from tests import utils


def test_validate_status_codes(client):

    position = test_positions.mock_position()

    # Get position list should give 200 OK
    data, status_code = test_positions.get_positions(client=client)
    assert status_code == 200

    # For create methods we expect 201 Created
    data, status_code = test_positions.create_position(client=client,
                                                       position=position)
    assert status_code == 201
    fen = data["fen"]

    # Retrieve, we expect 200 OK here.
    data, status_code = test_positions.get_position(client=client, fen=fen)
    assert status_code == 200

    # Delete, since we are returning the deleted position, a 200 OK is expected
    # instead of 204 No Content.
    data, status_code = test_positions.delete_position(client=client, fen=fen)
    assert status_code == 200


def test_validate_payload(client):
    position = test_positions.mock_position()

    # Check if the payload when creating a position matches what we thing.
    data, _ = test_positions.create_position(client=client, position=position)

    # API should save the email as lowercase.
    test_positions.no_state_change(data=data, position=position)

    # Check if the provided fen (UUID4) is valid
    fen = data["fen"]
    # Check if valid fen TODO

    data, _ = test_positions.get_position(client=client, fen=fen)
    test_positions.no_state_change(data=data, position=position, fen=fen)

    # Delete, since we are returning the deleted position, a 200 OK is expected
    data, status_code = test_positions.delete_position(client=client, fen=fen)
    test_positions.no_state_change(data=data, position=position, fen=fen)


def test_validate_headers(client):
    pass


def test_performance_sanity(client):
    mock_position = test_positions.mock_position()

    @utils.time_it
    def create(c, u):
        return test_positions.create_position(client=c, position=u)

    position, _ = create(c=client, u=mock_position)

    @utils.time_it
    def get(c, fen: pydantic.UUID4):
        return test_positions.get_position(client=c, fen=fen)

    get(c=client, fen=position["fen"])

    @utils.time_it
    def delete(c, fen: pydantic.UUID4):
        return test_positions.delete_position(client=c, fen=fen)
