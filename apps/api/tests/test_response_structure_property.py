"""
Property-based tests for response structure integrity

This test file uses Hypothesis to verify that the API returns responses with
the correct structure: exactly 3 Code_Smell objects in the smells list and
a summary field with at least 10 characters.

**Feature: mock-agent-api, Property 6: 响应结构完整性**
**Validates: Requirements 4.3, 4.4, 4.5**
"""

from hypothesis import given, strategies as st, settings, HealthCheck
from fastapi.testclient import TestClient


def get_client():
    """Helper function to create a FastAPI test client"""
    from main import app

    return TestClient(app)


class TestResponseStructureIntegrity:
    """Property-based tests for response structure integrity"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=10000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_response_contains_exactly_3_smells(self, code):
        """
        Property: Any valid request should return exactly 3 Code_Smell objects

        This test verifies that the API always returns exactly 3 code smells
        in the response, as specified in requirement 4.5.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code (length {len(code)}), got {response.status_code}"
        )

        # Verify response contains smells field
        data = response.json()
        assert "smells" in data, "Response should contain 'smells' field"

        # Verify smells list contains exactly 3 elements
        smells = data["smells"]
        assert isinstance(smells, list), (
            f"Expected smells to be a list, got {type(smells)}"
        )
        assert len(smells) == 3, f"Expected exactly 3 smells, got {len(smells)}"

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=10000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        ),
        language=st.text(min_size=0, max_size=50),
    )
    def test_response_summary_has_minimum_length(self, code, language):
        """
        Property: Any valid request should return a summary with at least 10 characters

        This test verifies that the API always returns a summary field with
        at least 10 characters, as specified in requirement 4.4.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code (length {len(code)}), got {response.status_code}"
        )

        # Verify response contains summary field
        data = response.json()
        assert "summary" in data, "Response should contain 'summary' field"

        # Verify summary is a string
        summary = data["summary"]
        assert isinstance(summary, str), (
            f"Expected summary to be a string, got {type(summary)}"
        )

        # Verify summary has at least 10 characters
        assert len(summary) >= 10, (
            f"Expected summary length >= 10 characters, got {len(summary)}"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=10000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_response_structure_completeness(self, code):
        """
        Property: Any valid request should return a complete response structure

        This test verifies that the API returns a response with all required fields:
        - status field (should be "success")
        - smells list with exactly 3 elements
        - summary field with at least 10 characters
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code (length {len(code)}), got {response.status_code}"
        )

        # Verify response structure
        data = response.json()

        # Verify all required fields are present
        assert "status" in data, "Response should contain 'status' field"
        assert "smells" in data, "Response should contain 'smells' field"
        assert "summary" in data, "Response should contain 'summary' field"

        # Verify status is "success"
        assert data["status"] == "success", (
            f"Expected status='success', got status='{data['status']}'"
        )

        # Verify smells list has exactly 3 elements
        smells = data["smells"]
        assert isinstance(smells, list), (
            f"Expected smells to be a list, got {type(smells)}"
        )
        assert len(smells) == 3, f"Expected exactly 3 smells, got {len(smells)}"

        # Verify summary has at least 10 characters
        summary = data["summary"]
        assert isinstance(summary, str), (
            f"Expected summary to be a string, got {type(summary)}"
        )
        assert len(summary) >= 10, (
            f"Expected summary length >= 10 characters, got {len(summary)}"
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
        language=st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
        ),
    )
    def test_response_structure_with_various_languages(self, code, language):
        """
        Property: Response structure should be consistent regardless of language

        This test verifies that the API returns the same structure (3 smells, summary >= 10 chars)
        regardless of the programming language specified in the request.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid request with language '{language}', got {response.status_code}"
        )

        # Verify response structure
        data = response.json()

        # Verify smells list has exactly 3 elements
        assert "smells" in data, "Response should contain 'smells' field"
        smells = data["smells"]
        assert len(smells) == 3, (
            f"Expected exactly 3 smells for language '{language}', got {len(smells)}"
        )

        # Verify summary has at least 10 characters
        assert "summary" in data, "Response should contain 'summary' field"
        summary = data["summary"]
        assert len(summary) >= 10, (
            f"Expected summary length >= 10 characters for language '{language}', got {len(summary)}"
        )


class TestSmellsListStructure:
    """Property-based tests specifically for the smells list structure"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=10000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_smells_list_is_not_empty(self, code):
        """
        Property: The smells list should never be empty

        This test verifies that the API always returns at least 1 smell,
        as specified in requirement 4.3.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        # Verify smells list is not empty
        data = response.json()
        smells = data["smells"]
        assert len(smells) >= 1, f"Expected at least 1 smell, got {len(smells)}"

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=10000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_each_smell_is_a_valid_object(self, code):
        """
        Property: Each smell in the list should be a valid object with required fields

        This test verifies that each smell in the response is a properly structured
        object (dictionary) with the expected fields.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        # Verify each smell is a valid object
        data = response.json()
        smells = data["smells"]

        for i, smell in enumerate(smells):
            assert isinstance(smell, dict), (
                f"Expected smell {i} to be a dict, got {type(smell)}"
            )

            # Verify required fields are present
            required_fields = ["type", "severity", "line", "message", "suggestion"]
            for field in required_fields:
                assert field in smell, f"Smell {i} should contain '{field}' field"

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(code_length=st.integers(min_value=1, max_value=10000))
    def test_smells_count_is_consistent_across_code_lengths(self, code_length):
        """
        Property: The number of smells should be consistent (3) regardless of code length

        This test verifies that the API returns exactly 3 smells regardless of
        the length of the input code.
        """
        client = get_client()
        code = "x" * code_length
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for code length {code_length}, got {response.status_code}"
        )

        # Verify smells count is exactly 3
        data = response.json()
        smells = data["smells"]
        assert len(smells) == 3, (
            f"Expected exactly 3 smells for code length {code_length}, got {len(smells)}"
        )


class TestSummaryFieldStructure:
    """Property-based tests specifically for the summary field structure"""

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        code=st.text(
            min_size=1,
            max_size=10000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        )
    )
    def test_summary_is_non_empty_string(self, code):
        """
        Property: The summary field should always be a non-empty string

        This test verifies that the summary field is always a string with
        at least 10 characters (as per requirement 4.4).
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        # Verify summary is a non-empty string
        data = response.json()
        summary = data["summary"]

        assert isinstance(summary, str), (
            f"Expected summary to be a string, got {type(summary)}"
        )
        assert len(summary) > 0, "Expected summary to be non-empty"
        assert len(summary) >= 10, (
            f"Expected summary length >= 10 characters, got {len(summary)}"
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
        language=st.sampled_from(
            ["python", "javascript", "java", "go", "rust", "c++", "c#", "ruby"]
        ),
    )
    def test_summary_contains_meaningful_content(self, code, language):
        """
        Property: The summary field should contain meaningful content

        This test verifies that the summary field is not just padding characters
        but contains actual meaningful content (at least 10 characters).
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for valid request, got {response.status_code}"
        )

        # Verify summary has meaningful content
        data = response.json()
        summary = data["summary"]

        # Summary should have at least 10 characters
        assert len(summary) >= 10, (
            f"Expected summary length >= 10 characters, got {len(summary)}"
        )

        # Summary should not be just whitespace
        assert summary.strip(), "Expected summary to contain non-whitespace content"


class TestBoundaryConditions:
    """Property-based tests for boundary conditions of response structure"""

    def test_minimum_code_length_returns_valid_structure(self):
        """
        Property: Minimum valid code (1 character) should return valid structure

        This test verifies that even with the smallest valid input,
        the API returns a properly structured response with 3 smells and summary >= 10 chars.
        """
        client = get_client()
        response = client.post("/api/review", json={"code": "x", "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for minimum code length, got {response.status_code}"
        )

        # Verify response structure
        data = response.json()

        # Verify smells count
        assert len(data["smells"]) == 3, (
            f"Expected exactly 3 smells for minimum code, got {len(data['smells'])}"
        )

        # Verify summary length
        assert len(data["summary"]) >= 10, (
            f"Expected summary length >= 10 for minimum code, got {len(data['summary'])}"
        )

    def test_maximum_code_length_returns_valid_structure(self):
        """
        Property: Maximum valid code (100,000 characters) should return valid structure

        This test verifies that even with the largest valid input,
        the API returns a properly structured response with 3 smells and summary >= 10 chars.

        Note: This test may take a moment due to the large payload.
        """
        client = get_client()
        code = "x" * 100000
        response = client.post("/api/review", json={"code": code, "language": "python"})

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for maximum code length, got {response.status_code}"
        )

        # Verify response structure
        data = response.json()

        # Verify smells count
        assert len(data["smells"]) == 3, (
            f"Expected exactly 3 smells for maximum code, got {len(data['smells'])}"
        )

        # Verify summary length
        assert len(data["summary"]) >= 10, (
            f"Expected summary length >= 10 for maximum code, got {len(data['summary'])}"
        )

    def test_empty_language_returns_valid_structure(self):
        """
        Property: Empty language string should return valid structure

        This test verifies that when language is an empty string,
        the API still returns a properly structured response.
        """
        client = get_client()
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": ""}
        )

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for empty language, got {response.status_code}"
        )

        # Verify response structure
        data = response.json()

        # Verify smells count
        assert len(data["smells"]) == 3, (
            f"Expected exactly 3 smells for empty language, got {len(data['smells'])}"
        )

        # Verify summary length
        assert len(data["summary"]) >= 10, (
            f"Expected summary length >= 10 for empty language, got {len(data['summary'])}"
        )

    def test_omitted_language_returns_valid_structure(self):
        """
        Property: Omitted language field should return valid structure

        This test verifies that when language field is omitted (using default),
        the API still returns a properly structured response.
        """
        client = get_client()
        response = client.post(
            "/api/review",
            json={"code": "def test(): pass"},  # No language field
        )

        # Verify HTTP 200 status code
        assert response.status_code == 200, (
            f"Expected 200 for omitted language, got {response.status_code}"
        )

        # Verify response structure
        data = response.json()

        # Verify smells count
        assert len(data["smells"]) == 3, (
            f"Expected exactly 3 smells for omitted language, got {len(data['smells'])}"
        )

        # Verify summary length
        assert len(data["summary"]) >= 10, (
            f"Expected summary length >= 10 for omitted language, got {len(data['summary'])}"
        )
