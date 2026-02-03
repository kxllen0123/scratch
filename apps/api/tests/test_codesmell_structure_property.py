"""
Property-based tests for Code Smell structure and content validation

This test file uses Hypothesis to verify that:
1. All Code_Smell objects have valid structure (Property 7)
2. Mock data is consistent across requests (Property 8)
3. Summary field contains accurate information (Property 9)

**Feature: mock-agent-api, Property 7, 8, 9: Code Smell 结构和内容验证**
**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6**
"""

from hypothesis import given, strategies as st, settings, HealthCheck
from fastapi.testclient import TestClient


def get_client():
    """Helper function to create a FastAPI test client"""
    from main import app

    return TestClient(app)


class TestCodeSmellStructureValidity:
    """
    Property-based tests for Code Smell structure validity

    **Property 7: Code Smell 结构有效性**
    **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
    """

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
    def test_all_smells_have_valid_type_field(self, code):
        """
        Property: Every Code_Smell object should have a type field with length >= 3 characters

        This test verifies that all returned Code_Smell objects have a valid 'type' field
        that meets the minimum length constraint (>= 3 characters).

        **Validates: Requirement 5.1**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        for i, smell in enumerate(smells):
            assert "type" in smell, f"Smell {i} should contain 'type' field"
            assert isinstance(smell["type"], str), (
                f"Smell {i} type should be a string, got {type(smell['type'])}"
            )
            assert len(smell["type"]) >= 3, (
                f"Smell {i} type should have length >= 3, got {len(smell['type'])} ('{smell['type']}')"
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
    def test_all_smells_have_valid_severity_field(self, code):
        """
        Property: Every Code_Smell object should have a severity field with value "low", "medium", or "high"

        This test verifies that all returned Code_Smell objects have a valid 'severity' field
        that is one of the allowed values.

        **Validates: Requirement 5.2**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]
        allowed_severities = {"low", "medium", "high"}

        for i, smell in enumerate(smells):
            assert "severity" in smell, f"Smell {i} should contain 'severity' field"
            assert isinstance(smell["severity"], str), (
                f"Smell {i} severity should be a string, got {type(smell['severity'])}"
            )
            assert smell["severity"] in allowed_severities, (
                f"Smell {i} severity should be one of {allowed_severities}, got '{smell['severity']}'"
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
    def test_all_smells_have_valid_line_field(self, code):
        """
        Property: Every Code_Smell object should have a line field that is an integer > 0

        This test verifies that all returned Code_Smell objects have a valid 'line' field
        that is a positive integer.

        **Validates: Requirement 5.3**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        for i, smell in enumerate(smells):
            assert "line" in smell, f"Smell {i} should contain 'line' field"
            assert isinstance(smell["line"], int), (
                f"Smell {i} line should be an integer, got {type(smell['line'])}"
            )
            assert smell["line"] > 0, (
                f"Smell {i} line should be > 0, got {smell['line']}"
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
    def test_all_smells_have_valid_message_field(self, code):
        """
        Property: Every Code_Smell object should have a message field with length >= 5 characters

        This test verifies that all returned Code_Smell objects have a valid 'message' field
        that meets the minimum length constraint (>= 5 characters).

        **Validates: Requirement 5.4**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        for i, smell in enumerate(smells):
            assert "message" in smell, f"Smell {i} should contain 'message' field"
            assert isinstance(smell["message"], str), (
                f"Smell {i} message should be a string, got {type(smell['message'])}"
            )
            assert len(smell["message"]) >= 5, (
                f"Smell {i} message should have length >= 5, got {len(smell['message'])} ('{smell['message']}')"
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
    def test_all_smells_have_valid_suggestion_field(self, code):
        """
        Property: Every Code_Smell object should have a suggestion field with length >= 10 characters

        This test verifies that all returned Code_Smell objects have a valid 'suggestion' field
        that meets the minimum length constraint (>= 10 characters).

        **Validates: Requirement 5.5**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        for i, smell in enumerate(smells):
            assert "suggestion" in smell, f"Smell {i} should contain 'suggestion' field"
            assert isinstance(smell["suggestion"], str), (
                f"Smell {i} suggestion should be a string, got {type(smell['suggestion'])}"
            )
            assert len(smell["suggestion"]) >= 10, (
                f"Smell {i} suggestion should have length >= 10, got {len(smell['suggestion'])} ('{smell['suggestion']}')"
            )

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
    def test_all_smells_have_complete_structure(self, code, language):
        """
        Property: Every Code_Smell object should have all required fields with valid constraints

        This test verifies that all returned Code_Smell objects have complete structure
        with all fields meeting their respective constraints.

        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]
        allowed_severities = {"low", "medium", "high"}

        for i, smell in enumerate(smells):
            # Verify all required fields are present
            required_fields = ["type", "severity", "line", "message", "suggestion"]
            for field in required_fields:
                assert field in smell, f"Smell {i} should contain '{field}' field"

            # Verify type field
            assert isinstance(smell["type"], str) and len(smell["type"]) >= 3, (
                f"Smell {i} type invalid: '{smell['type']}'"
            )

            # Verify severity field
            assert smell["severity"] in allowed_severities, (
                f"Smell {i} severity invalid: '{smell['severity']}'"
            )

            # Verify line field
            assert isinstance(smell["line"], int) and smell["line"] > 0, (
                f"Smell {i} line invalid: {smell['line']}"
            )

            # Verify message field
            assert isinstance(smell["message"], str) and len(smell["message"]) >= 5, (
                f"Smell {i} message invalid: '{smell['message']}'"
            )

            # Verify suggestion field
            assert (
                isinstance(smell["suggestion"], str) and len(smell["suggestion"]) >= 10
            ), f"Smell {i} suggestion invalid: '{smell['suggestion']}'"


class TestMockDataConsistency:
    """
    Property-based tests for mock data consistency

    **Property 8: 模拟数据一致性**
    **Validates: Requirements 6.1, 6.2, 6.3**
    """

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
    def test_first_smell_is_always_long_method(self, code):
        """
        Property: The first Code_Smell should always be "Long Method" with severity="medium" at line 10

        This test verifies that the API consistently returns the first predefined smell
        as specified in the requirements.

        **Validates: Requirement 6.1**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        assert len(smells) >= 1, "Response should contain at least 1 smell"

        first_smell = smells[0]
        assert first_smell["type"] == "Long Method", (
            f"First smell type should be 'Long Method', got '{first_smell['type']}'"
        )
        assert first_smell["severity"] == "medium", (
            f"First smell severity should be 'medium', got '{first_smell['severity']}'"
        )
        assert first_smell["line"] == 10, (
            f"First smell line should be 10, got {first_smell['line']}"
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
    def test_second_smell_is_always_magic_number(self, code):
        """
        Property: The second Code_Smell should always be "Magic Number" with severity="low" at line 15

        This test verifies that the API consistently returns the second predefined smell
        as specified in the requirements.

        **Validates: Requirement 6.2**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        assert len(smells) >= 2, "Response should contain at least 2 smells"

        second_smell = smells[1]
        assert second_smell["type"] == "Magic Number", (
            f"Second smell type should be 'Magic Number', got '{second_smell['type']}'"
        )
        assert second_smell["severity"] == "low", (
            f"Second smell severity should be 'low', got '{second_smell['severity']}'"
        )
        assert second_smell["line"] == 15, (
            f"Second smell line should be 15, got {second_smell['line']}"
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
    def test_third_smell_is_always_duplicate_code(self, code):
        """
        Property: The third Code_Smell should always be "Duplicate Code" with severity="high" at line 25

        This test verifies that the API consistently returns the third predefined smell
        as specified in the requirements.

        **Validates: Requirement 6.3**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        assert len(smells) >= 3, "Response should contain at least 3 smells"

        third_smell = smells[2]
        assert third_smell["type"] == "Duplicate Code", (
            f"Third smell type should be 'Duplicate Code', got '{third_smell['type']}'"
        )
        assert third_smell["severity"] == "high", (
            f"Third smell severity should be 'high', got '{third_smell['severity']}'"
        )
        assert third_smell["line"] == 25, (
            f"Third smell line should be 25, got {third_smell['line']}"
        )

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
    def test_all_three_smells_are_consistent(self, code, language):
        """
        Property: All three Code_Smell objects should always be the same predefined values

        This test verifies that the API consistently returns all three predefined smells
        in the correct order with the correct attributes, regardless of input.

        **Validates: Requirements 6.1, 6.2, 6.3**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        assert len(smells) == 3, (
            f"Response should contain exactly 3 smells, got {len(smells)}"
        )

        # Verify first smell: Long Method
        assert smells[0]["type"] == "Long Method", (
            f"First smell type should be 'Long Method', got '{smells[0]['type']}'"
        )
        assert smells[0]["severity"] == "medium", (
            f"First smell severity should be 'medium', got '{smells[0]['severity']}'"
        )
        assert smells[0]["line"] == 10, (
            f"First smell line should be 10, got {smells[0]['line']}"
        )

        # Verify second smell: Magic Number
        assert smells[1]["type"] == "Magic Number", (
            f"Second smell type should be 'Magic Number', got '{smells[1]['type']}'"
        )
        assert smells[1]["severity"] == "low", (
            f"Second smell severity should be 'low', got '{smells[1]['severity']}'"
        )
        assert smells[1]["line"] == 15, (
            f"Second smell line should be 15, got {smells[1]['line']}"
        )

        # Verify third smell: Duplicate Code
        assert smells[2]["type"] == "Duplicate Code", (
            f"Third smell type should be 'Duplicate Code', got '{smells[2]['type']}'"
        )
        assert smells[2]["severity"] == "high", (
            f"Third smell severity should be 'high', got '{smells[2]['severity']}'"
        )
        assert smells[2]["line"] == 25, (
            f"Third smell line should be 25, got {smells[2]['line']}"
        )

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(code_length=st.integers(min_value=1, max_value=10000))
    def test_mock_data_consistency_across_code_lengths(self, code_length):
        """
        Property: Mock data should be consistent regardless of code length

        This test verifies that the three predefined smells are returned consistently
        regardless of the length of the input code.

        **Validates: Requirements 6.1, 6.2, 6.3**
        """
        client = get_client()
        code = "x" * code_length
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for code length {code_length}, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]

        # Verify the three predefined smells
        assert len(smells) == 3
        assert (
            smells[0]["type"] == "Long Method"
            and smells[0]["severity"] == "medium"
            and smells[0]["line"] == 10
        )
        assert (
            smells[1]["type"] == "Magic Number"
            and smells[1]["severity"] == "low"
            and smells[1]["line"] == 15
        )
        assert (
            smells[2]["type"] == "Duplicate Code"
            and smells[2]["severity"] == "high"
            and smells[2]["line"] == 25
        )


class TestSummaryFieldAccuracy:
    """
    Property-based tests for summary field accuracy

    **Property 9: Summary 字段准确性**
    **Validates: Requirements 6.4, 6.5, 6.6**
    """

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
    def test_summary_contains_exact_character_count(self, code):
        """
        Property: Summary should contain the exact character count of the submitted code

        This test verifies that the summary field accurately reports the number of
        characters in the submitted code.

        **Validates: Requirement 6.4**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        summary = data["summary"]

        # Verify summary contains the exact character count
        expected_count = len(code)
        assert str(expected_count) in summary, (
            f"Summary should contain character count {expected_count}, got: '{summary}'"
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
    def test_summary_contains_language_name(self, code, language):
        """
        Property: Summary should contain the programming language name from the request

        This test verifies that the summary field accurately includes the language
        specified in the request.

        **Validates: Requirement 6.5**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        summary = data["summary"]

        # Verify summary contains the language name
        assert language in summary, (
            f"Summary should contain language '{language}', got: '{summary}'"
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
    def test_summary_contains_smell_count(self, code):
        """
        Property: Summary should contain the exact count of detected smells (3)

        This test verifies that the summary field accurately reports the number of
        detected code smells.

        **Validates: Requirement 6.6**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        summary = data["summary"]
        smells = data["smells"]

        # Verify summary contains the smell count
        smell_count = len(smells)
        assert str(smell_count) in summary, (
            f"Summary should contain smell count {smell_count}, got: '{summary}'"
        )

        # Verify the count is 3 (as per mock data specification)
        assert smell_count == 3, f"Expected exactly 3 smells, got {smell_count}"

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
    def test_summary_contains_all_required_information(self, code, language):
        """
        Property: Summary should contain character count, language, and smell count

        This test verifies that the summary field contains all three required pieces
        of information: character count, language name, and smell count.

        **Validates: Requirements 6.4, 6.5, 6.6**
        """
        client = get_client()
        response = client.post("/api/review", json={"code": code, "language": language})

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        summary = data["summary"]

        # Verify summary contains character count
        char_count = len(code)
        assert str(char_count) in summary, (
            f"Summary should contain character count {char_count}, got: '{summary}'"
        )

        # Verify summary contains language
        assert language in summary, (
            f"Summary should contain language '{language}', got: '{summary}'"
        )

        # Verify summary contains smell count (should be 3)
        assert "3" in summary, f"Summary should contain smell count 3, got: '{summary}'"

    @settings(
        max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(code_length=st.integers(min_value=1, max_value=10000))
    def test_summary_accuracy_across_code_lengths(self, code_length):
        """
        Property: Summary should accurately reflect code length regardless of size

        This test verifies that the summary field accurately reports the character
        count for various code lengths.

        **Validates: Requirement 6.4**
        """
        client = get_client()
        code = "x" * code_length
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for code length {code_length}, got {response.status_code}"
        )

        data = response.json()
        summary = data["summary"]

        # Verify summary contains the exact character count
        assert str(code_length) in summary, (
            f"Summary should contain character count {code_length}, got: '{summary}'"
        )

    def test_summary_with_default_language(self):
        """
        Property: Summary should use default language "python" when language is omitted

        This test verifies that when the language field is omitted, the summary
        correctly uses the default language value.

        **Validates: Requirement 6.5**
        """
        client = get_client()
        code = "def test(): pass"
        response = client.post(
            "/api/review",
            json={"code": code},  # No language field
        )

        assert response.status_code == 200, (
            f"Expected 200 for valid code, got {response.status_code}"
        )

        data = response.json()
        summary = data["summary"]

        # Verify summary contains the default language "python"
        assert "python" in summary, (
            f"Summary should contain default language 'python', got: '{summary}'"
        )


class TestBoundaryConditions:
    """Property-based tests for boundary conditions of Code Smell structure and content"""

    def test_minimum_code_length_produces_valid_smells_and_summary(self):
        """
        Property: Minimum valid code (1 character) should produce valid smells and accurate summary

        This test verifies that even with the smallest valid input, all Code_Smell
        objects have valid structure and the summary is accurate.
        """
        client = get_client()
        code = "x"
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for minimum code length, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]
        summary = data["summary"]

        # Verify smells structure
        assert len(smells) == 3
        for smell in smells:
            assert len(smell["type"]) >= 3
            assert smell["severity"] in {"low", "medium", "high"}
            assert smell["line"] > 0
            assert len(smell["message"]) >= 5
            assert len(smell["suggestion"]) >= 10

        # Verify summary accuracy
        assert "1" in summary  # Character count
        assert "python" in summary  # Language
        assert "3" in summary  # Smell count

    def test_maximum_code_length_produces_valid_smells_and_summary(self):
        """
        Property: Maximum valid code (100,000 characters) should produce valid smells and accurate summary

        This test verifies that even with the largest valid input, all Code_Smell
        objects have valid structure and the summary is accurate.

        Note: This test may take a moment due to the large payload.
        """
        client = get_client()
        code = "x" * 100000
        response = client.post("/api/review", json={"code": code, "language": "python"})

        assert response.status_code == 200, (
            f"Expected 200 for maximum code length, got {response.status_code}"
        )

        data = response.json()
        smells = data["smells"]
        summary = data["summary"]

        # Verify smells structure
        assert len(smells) == 3
        for smell in smells:
            assert len(smell["type"]) >= 3
            assert smell["severity"] in {"low", "medium", "high"}
            assert smell["line"] > 0
            assert len(smell["message"]) >= 5
            assert len(smell["suggestion"]) >= 10

        # Verify summary accuracy
        assert "100000" in summary  # Character count
        assert "python" in summary  # Language
        assert "3" in summary  # Smell count
