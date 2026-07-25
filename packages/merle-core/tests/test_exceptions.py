"""
Tests for the merle_core exception hierarchy.
"""

from merle_core.exceptions import (
    ElementNotFoundError,
    MerleError,
    RetryExhaustedError,
    SecretNotFoundError,
)


def test_merle_error_base():
    err = MerleError("Something bad", details={"code": 42})
    assert str(err) == "Something bad"
    assert err.details == {"code": 42}


def test_retry_exhausted_error():
    original = ConnectionError("timeout")
    err = RetryExhaustedError("fetch_data", attempts=5, last_error=original)

    assert "fetch_data" in str(err)
    assert err.attempts == 5
    assert isinstance(err.last_error, ConnectionError)


def test_element_not_found_error_carries_context():
    err = ElementNotFoundError("#submit-button", page_url="https://app.example.com/form")

    assert "submit-button" in str(err)
    assert err.selector == "#submit-button"
    assert err.page_url == "https://app.example.com/form"


def test_secret_not_found_error():
    err = SecretNotFoundError("api-key")
    assert isinstance(err, MerleError)
