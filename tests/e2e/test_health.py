import pytest

from virtuals_sdk import GameSDK


@pytest.fixture
def game_sdk():
    return GameSDK(api_key="DUMMY")


def test_health_check_e2e(game_sdk):
    """Test the actual API health endpoint"""
    response = game_sdk.health()

    # Verify response structure
    assert isinstance(response, dict)
    assert "status" in response
    assert isinstance(response["status"], str)

    # Verify health status
    assert response["status"] == "ok"

    # Optional: Check if version is present and is a string
    if "version" in response:
        assert isinstance(response["version"], str)
