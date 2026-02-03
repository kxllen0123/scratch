"""
Property-based tests for valid request success responses

This test file uses Hypothesis to verify that the API correctly returns successful
responses (HTTP 200 with status="success") for all valid CodeReviewRequest inputs.
It generates various valid code and language combinations to ensure comprehensive coverage.

**Feature: mock-agent-api, Property 5: 有效请求返回成功响应**
**Validates: Requirements 4.1, 4.2**
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from fastapi.testclient import TestClient


def get_client():
    """Helper function to create a FastAPI test client"""
    from main import app

    return TestClient(app)


class TestValidRequestsReturnSuccess:
    """Property-based tests for valid request success responses"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=100000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_valid_code_returns_200_and_success_status(self, code):
        """
        Property: Any valid code string (1-100,000 chars) should return HTTP 200 with status="success"

        This test verifies that when a valid code string is provided (within length constraints),
        the API returns a successful response with HTTP 200 status code and status="success" in the body.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code (length {len(code)}), got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=1000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        ),
        language=st.text(min_size=0, max_size=50),
    )
    def test_valid_code_and_language_returns_200_and_success_status(
        self, code, language
    ):
        """
        Property: Any valid code and language combination should return HTTP 200 with status="success"

        This test verifies that when both valid code and language strings are provided,
        the API returns a successful response regardless of the language value.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code (length {len(code)}) and language '{language}', got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=1000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_valid_code_without_language_returns_200_and_success_status(self, code):
        """
        Property: Any valid code without language field should return HTTP 200 with status="success"

        This test verifies that when only valid code is provided (language field omitted),
        the API returns a successful response using the default language value.
        """
        client = get_client()
        response = client.post(
            "/api/review",
            json={"code": code},  # No language field
        )

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code (length {len(code)}) without language, got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.one_of(
            st.text(
                min_size=1,
                max_size=100,
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
            ),  # Alphanumeric
            st.text(
                min_size=1,
                max_size=100,
                alphabet=st.characters(whitelist_categories=("Zs", "Cc")),
            ),  # Whitespace
            st.text(
                min_size=1,
                max_size=100,
                alphabet=st.characters(whitelist_categories=("Po", "Ps", "Pe")),
            ),  # Punctuation
            st.text(
                min_size=1,
                max_size=100,
                alphabet=st.characters(blacklist_categories=("Cs",)),
            ),  # Mixed
        )
    )
    def test_various_character_types_return_200_and_success_status(self, code):
        """
        Property: Code with various character types should return HTTP 200 with status="success"

        This test verifies that the API handles code containing different character types
        (alphanumeric, whitespace, punctuation, unicode) correctly.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for code with various characters (length {len(code)}), got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        language=st.sampled_from(
            [
                "python",
                "javascript",
                "java",
                "go",
                "rust",
                "c++",
                "c#",
                "ruby",
                "php",
                "swift",
                "kotlin",
                "typescript",
                "scala",
                "perl",
                "r",
                "matlab",
                "shell",
                "powershell",
                "sql",
                "html",
                "css",
            ]
        )
    )
    def test_common_programming_languages_return_200_and_success_status(self, language):
        """
        Property: Common programming language values should return HTTP 200 with status="success"

        This test verifies that the API handles common programming language identifiers correctly.
        """
        client = get_client()
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": language}
        )

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for language '{language}', got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert data["status"] == "success", (
            f"Expected status='success' for language '{language}', got status='{data['status']}'"
        )


class TestValidRequestResponseStructure:
    """Property-based tests verifying response structure for valid requests"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=1000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_valid_request_returns_complete_response_structure(self, code):
        """
        Property: Valid requests should return responses with all required fields

        This test verifies that successful responses contain all required fields:
        status, smells, and summary.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        # Verify response structure
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert "smells" in data, "Response should contain 'smells' field"
        assert "summary" in data, "Response should contain 'summary' field"

        # Verify status is "success"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

        # Verify smells is a list
        assert isinstance(data["smells"], list), (
            f"Expected smells to be a list, got {type(data['smells'])}"
        )

        # Verify summary is a string
        assert isinstance(data["summary"], str), (
            f"Expected summary to be a string, got {type(data['summary'])}"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=1000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        ),
        language=st.text(min_size=0, max_size=50),
    )
    def test_valid_request_response_is_json_serializable(self, code, language):
        """
        Property: Valid request responses should be properly JSON serializable

        This test verifies that the API returns valid JSON responses that can be
        parsed and accessed without errors.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid request, got {response.status_code}"
        )

        # Verify response can be parsed as JSON
        try:
            data = response.json()
        except Exception as e:
            pytest.fail(f"Failed to parse response as JSON: {e}")

        # Verify status field is accessible and equals "success"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )


class TestBoundaryConditions:
    """Property-based tests for boundary conditions of valid requests"""

    def test_minimum_valid_code_length_returns_200_and_success(self):
        """
        Property: Code with minimum valid length (1 character) should return HTTP 200 with status="success"

        This test verifies that the API handles the smallest valid code input correctly.
        """
        client = get_client()
        response = client.post(
            "/api/review",
            json={"code": "x", "language": "python"},  # Minimum 1 character
        )

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for minimum valid code length, got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

    def test_maximum_valid_code_length_returns_200_and_success(self):
        """
        Property: Code with maximum valid length (100,000 characters) should return HTTP 200 with status="success"

        This test verifies that the API handles the largest valid code input correctly.

        Note: This test may take a moment due to the large payload.
        """
        client = get_client()
        code = "x" * 100000  # Maximum 100,000 characters
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for maximum valid code length, got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(code_length=st.integers(min_value=1, max_value=10000))
    def test_various_valid_code_lengths_return_200_and_success(self, code_length):
        """
        Property: Code with any valid length (1-100,000) should return HTTP 200 with status="success"

        This test verifies that the API handles code of various valid lengths correctly.
        """
        client = get_client()
        code = "x" * code_length
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for code length {code_length}, got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert data["status"] == "success", (
            f"Expected status='success' for code length {code_length}, got status='{data['status']}'"
        )

    def test_empty_language_string_returns_200_and_success(self):
        """
        Property: Empty language string should return HTTP 200 with status="success"

        This test verifies that the API accepts empty string as a valid language value.
        """
        client = get_client()
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": ""}
        )

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for empty language string, got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )


class TestRealWorldCodeSamples:
    """Property-based tests using realistic code samples"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code_pattern=st.sampled_from(
            [
                "def {name}(): pass",
                "class {name}: pass",
                "import {name}",
                "from {name} import *",
                "x = {name}",
                "# {name}",
                "print('{name}')",
                "if {name}: pass",
                "for {name} in range(10): pass",
                "while {name}: break",
            ]
        ),
        name=st.text(
            min_size=1,
            max_size=20,
            alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
        ),
    )
    def test_realistic_python_code_patterns_return_200_and_success(
        self, code_pattern, name
    ):
        """
        Property: Realistic Python code patterns should return HTTP 200 with status="success"

        This test verifies that the API handles realistic Python code structures correctly.
        """
        client = get_client()
        code = code_pattern.format(name=name)
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for realistic code pattern '{code}', got {response.status_code}"
        )

        # Verify response body contains status="success"
        data = response.json()
        assert data["status"] == "success", (
            f"Expected status='success' for code '{code}', got status='{data['status']}'"
        )
