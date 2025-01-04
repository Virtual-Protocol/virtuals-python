import pytest
import responses

from virtuals_sdk import GameSDK


@pytest.fixture
def game_sdk():
    return GameSDK(api_key="test-api-key")


@responses.activate
def test_health_check(game_sdk):
    # Mock the health check endpoint response
    responses.add(
        responses.GET,
        "https://game-api.virtuals.io/api/health",
        json={"status": "healthy", "version": "1.0.0"},
        status=200,
    )

    # Call the health check endpoint
    response = game_sdk.health()

    # Verify the response
    assert response["status"] == "healthy"
    assert response["version"] == "1.0.0"

    # Verify the request
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://game-api.virtuals.io/api/health"
    assert responses.calls[0].request.headers["x-api-key"] == "test-api-key"
