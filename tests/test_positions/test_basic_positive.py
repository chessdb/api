"""Basic positive tests (happy paths).

This module executes API calls with valid required parameters.

Validation checks:
    Validate status code: All requests should return 2XX HTTP status codes.
    Validate payload: Response is a well-formed JSON object.
    Validate state: GET requests should not change state.
    Validate headers: Verifies if headers are the same as expected.
"""

import pydantic
import pytest
from requests import exceptions

from tests import test_positions, utils


def test_validate_status_codes(client):

    position = test_positions.mock_position()

    # Get position list should give 200 OK
    data, status_code = test_positions.get_positiones(client=client)
    assert status_code == 200

    # For create methods we expect 201 Created
    data, status_code = test_positions.create_position(client=client,
                                                       position=position)
    assert status_code == 201
    identifier = data["identifier"]

    # Retrieve, we expect 200 OK here.
    data, status_code = test_positions.get_position(client=client,
                                                    identifier=identifier)
    assert status_code == 200

    # We expect 200 OK from updates.
    update_position = position
    update_position["street_position"] = "Test Testsen 100"
    _, status_code = test_positions.update_position(client=client,
                                                    position=data,
                                                    identifier=identifier)
    assert status_code == 200

    # Delete, since we are returning the deleted position, a 200 OK is expected
    # instead of 204 No Content.
    data, status_code = test_positions.delete_position(client=client,
                                                       identifier=identifier)
    assert status_code == 200


def test_validate_payload(client):
    position = test_positions.mock_position()

    # Check if the payload when creating a position matches what we thing.
    data, _ = test_positions.create_position(client=client, position=position)

    # API should save the email as lowercase.
    test_positions.no_state_change(data=data, position=position)

    # Check if the provided identifier (UUID4) is valid
    identifier = data["identifier"]
    try:
        pydantic.UUID4(identifier)
    except pydantic.ValidationError:
        pytest.fail("Not a valid UUID4")

    # Check if the state is the same.
    data, _ = test_positions.get_position(client=client, identifier=identifier)
    test_positions.no_state_change(data=data,
                                   position=position,
                                   identifier=identifier)

    # Delete, since we are returning the deleted position, a 200 OK is expected
    data, status_code = test_positions.delete_position(client=client,
                                                       identifier=identifier)
    test_positions.no_state_change(data=data,
                                   position=position,
                                   identifier=identifier)


def test_validate_headers(client):
    pass


def test_performance_sanity(client):
    mock_position = test_positions.mock_position()

    @utils.time_it
    def create(c, u):
        return test_positions.create_position(client=c, position=u)

    position, _ = create(c=client, u=mock_position)

    @utils.time_it
    def get(c, identifier: pydantic.UUID4):
        return test_positions.get_position(client=c, identifier=identifier)

    get(c=client, identifier=position["identifier"])

    @utils.time_it
    def delete(c, identifier: pydantic.UUID4):
        return test_positions.delete_position(client=c, identifier=identifier)
