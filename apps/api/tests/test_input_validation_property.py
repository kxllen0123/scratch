"""
Property-based tests for input validation

This test file uses Hypothesis to verify that the API correctly rejects invalid requests
with HTTP 422 status code. It generates various types of invalid inputs to ensure
comprehensive validation coverage.

**Feature: mock-agent-api, Property 3: 输入验证拒绝无效请求**
**Validates: Requirements 3.2, 3.4, 7.3**
"""

from hypothesis import given, strategies as st, settings, HealthCheck
from fastapi.testclient import TestClient


def get_client():
    """Helper function to create a FastAPI test client"""
    from main import app

    return TestClient(app)


class TestInvalidRequestsReturn422:
    """Property-based tests for invalid request validation"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.one_of(
            st.none(),  # Missing code field (will be handled by not including it)
            st.integers(),  # Wrong type - integer instead of string
            st.floats(
                allow_nan=False, allow_infinity=False
            ),  # Wrong type - float instead of string (no inf/nan)
            st.booleans(),  # Wrong type - boolean instead of string
            st.lists(st.text()),  # Wrong type - list instead of string
            st.dictionaries(
                st.text(), st.text()
            ),  # Wrong type - dict instead of string
        )
    )
    def test_invalid_code_type_returns_422(self, code):
        """
        Property: Any request with invalid code type should return HTTP 422

        This test verifies that when the 'code' field has an incorrect type
        (not a string), the API returns a 422 validation error.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})
        assert response.status_code == 422, (
            f"Expected 422 for invalid code type {type(code)}, got {response.status_code}"
        )

    def test_code_exceeding_max_length_returns_422(self):
        """
        Property: Any request with code exceeding 100,000 characters should return HTTP 422

        This test verifies that the API enforces the maximum code length constraint
        and rejects requests that exceed it.

        Note: We test this with a fixed example rather than generating large strings
        because Hypothesis has limitations on generating very large text.
        """
        client = get_client()
        # Create a string that exceeds 100,000 characters
        code = "x" * 100001
        response = client.post("/api/review", json={"code": code, "language": "python"})
        assert response.status_code == 422, (
            f"Expected 422 for code length {len(code)}, got {response.status_code}"
        )

        # Verify error message mentions the length constraint
        error_detail = response.json()
        assert "detail" in error_detail

    def test_missing_code_field_returns_422(self):
        """
        Property: Any request missing the required 'code' field should return HTTP 422

        This test verifies that the API rejects requests that don't include
        the mandatory 'code' field.
        """
        client = get_client()
        response = client.post(
            "/api/review",
            json={"language": "python"},  # Missing 'code' field
        )
        assert response.status_code == 422, (
            f"Expected 422 for missing code field, got {response.status_code}"
        )

        # Verify error detail mentions the missing field
        error_detail = response.json()
        assert "detail" in error_detail
        # Check that the error is about the 'code' field
        error_str = str(error_detail)
        assert "code" in error_str.lower()

    def test_empty_string_code_returns_422(self):
        """
        Property: Any request with empty string code should return HTTP 422

        This test verifies that the API rejects requests with an empty code string,
        as per the min_length=1 constraint.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": "", "language": "python"})
        assert response.status_code == 422, (
            f"Expected 422 for empty code string, got {response.status_code}"
        )

        # Verify error detail mentions the validation issue
        error_detail = response.json()
        assert "detail" in error_detail

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        language=st.one_of(
            st.integers(),  # Wrong type - integer instead of string
            st.floats(
                allow_nan=False, allow_infinity=False
            ),  # Wrong type - float instead of string (no inf/nan)
            st.booleans(),  # Wrong type - boolean instead of string
            st.lists(st.text()),  # Wrong type - list instead of string
            st.dictionaries(
                st.text(), st.text()
            ),  # Wrong type - dict instead of string
        )
    )
    def test_invalid_language_type_returns_422(self, language):
        """
        Property: Any request with invalid language type should return HTTP 422

        This test verifies that when the 'language' field has an incorrect type
        (not a string), the API returns a 422 validation error.
        """
        client = get_client()
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": language}
        )
        assert response.status_code == 422, (
            f"Expected 422 for invalid language type {type(language)}, got {response.status_code}"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        invalid_json=st.one_of(
            st.text(min_size=1, max_size=100).filter(
                lambda x: x not in ["null", "true", "false"]
            ),  # Random text that's not valid JSON
            st.just("not a json"),
            st.just("{invalid}"),
            st.just("[1, 2, 3]"),  # Valid JSON but wrong structure
        )
    )
    def test_malformed_json_returns_422(self, invalid_json):
        """
        Property: Any request with malformed JSON should return HTTP 422

        This test verifies that the API properly handles and rejects
        requests with invalid JSON payloads.
        """
        client = get_client()
        response = client.post(
            "/api/review",
            data=invalid_json,  # Send as raw data, not JSON
            headers={"Content-Type": "application/json"},
        )
        # Should return 422 for validation error or 400 for bad request
        assert response.status_code in [400, 422], (
            f"Expected 400 or 422 for malformed JSON, got {response.status_code}"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        extra_field_value=st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.booleans(),
        )
    )
    def test_extra_fields_are_handled(self, extra_field_value):
        """
        Property: Requests with extra fields should be handled gracefully

        This test verifies that the API either accepts or rejects requests
        with extra fields consistently. By default, Pydantic ignores extra fields.
        """
        client = get_client()
        response = client.post(
            "/api/review",
            json={
                "code": "def test(): pass",
                "language": "python",
                "extra_field": extra_field_value,
            },
        )
        # Should either accept (200) or reject (422), but not crash (500)
        assert response.status_code in [200, 422], (
            f"Expected 200 or 422, got {response.status_code}"
        )
        assert response.status_code != 500, "Server should not crash on extra fields"


class TestCombinedInvalidInputs:
    """Property-based tests for combinations of invalid inputs"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.one_of(
            st.just("x" * 100001),  # Too long - use fixed example
            st.just(""),  # Empty
            st.integers(),  # Wrong type
        ),
        language=st.one_of(
            st.text(min_size=0, max_size=50),  # Valid or empty string
            st.integers(),  # Wrong type
            st.none(),  # Missing (will be omitted)
        ),
    )
    def test_multiple_validation_errors_return_422(self, code, language):
        """
        Property: Requests with multiple validation errors should return HTTP 422

        This test verifies that the API correctly handles requests with
        multiple validation issues and returns a comprehensive error response.
        """
        client = get_client()
        request_data = {"code": code}
        if language is not None:
            request_data["language"] = language

        response = client.post("/api/review", json=request_data)

        # If code is valid string and language is valid or default, should succeed
        is_code_valid = isinstance(code, str) and 1 <= len(code) <= 100000
        is_language_valid = language is None or isinstance(language, str)

        if is_code_valid and is_language_valid:
            assert response.status_code == 200, (
                f"Expected 200 for valid input, got {response.status_code}"
            )
        else:
            assert response.status_code == 422, (
                f"Expected 422 for invalid input, got {response.status_code}"
            )

            # Verify error response has detail field
            error_detail = response.json()
            assert "detail" in error_detail


class TestEdgeCases:
    """Property-based tests for edge cases in input validation"""

    def test_code_at_max_length_boundary(self):
        """
        Property: Code at exactly 100,000 characters should be accepted

        This test verifies that the API correctly handles code at the
        maximum allowed length boundary.

        Note: We test specific boundary values rather than generating large strings
        because Hypothesis has limitations on generating very large text.
        """
        client = get_client()

        # Test at exactly 100,000 characters (should be accepted)
        code_at_limit = "x" * 100000
        response = client.post(
            "/api/review", json={"code": code_at_limit, "language": "python"}
        )
        assert response.status_code == 200, (
            f"Expected 200 for code length {len(code_at_limit)}, got {response.status_code}"
        )

        # Test at 100,001 characters (should be rejected)
        code_over_limit = "x" * 100001
        response = client.post(
            "/api/review", json={"code": code_over_limit, "language": "python"}
        )
        assert response.status_code == 422, (
            f"Expected 422 for code length {len(code_over_limit)}, got {response.status_code}"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            alphabet=st.characters(blacklist_categories=("Cs",)),
            min_size=1,
            max_size=1000,
        )
    )
    def test_code_with_special_characters(self, code):
        """
        Property: Code with various special characters should be handled correctly

        This test verifies that the API can handle code containing
        special characters, unicode, etc.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Should succeed if length is valid
        if 1 <= len(code) <= 100000:
            assert response.status_code == 200, (
                f"Expected 200 for valid code with special chars, got {response.status_code}"
            )
        else:
            assert response.status_code == 422, (
                f"Expected 422 for invalid code length, got {response.status_code}"
            )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(language=st.text(min_size=0, max_size=100))
    def test_various_language_values(self, language):
        """
        Property: Various language string values should be accepted

        This test verifies that the API accepts any string value for the
        language field (no enum constraint on language).
        """
        client = get_client()
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": language}
        )

        # Should succeed for any string language value
        assert response.status_code == 200, (
            f"Expected 200 for language '{language}', got {response.status_code}"
        )
