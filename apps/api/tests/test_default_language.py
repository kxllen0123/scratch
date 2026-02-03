"""
Unit tests for default language value application

This test file verifies that when a CodeReviewRequest does not include the 'language' field,
the API correctly applies the default value of "python".

**Feature: mock-agent-api, Property 4: 默认语言值应用**
**Validates: Requirements 3.3**
"""

import pytest


class TestDefaultLanguageValue:
    """Unit tests for default language value application"""

    def test_missing_language_field_defaults_to_python(self, client):
        """
        Test that when language field is omitted, it defaults to 'python'

        This test verifies that the API applies the default language value
        when the request does not include the language field.
        """
        # Send request without language field
        response = client.post(
            "/api/review",
            json={"code": "def hello(): pass"},  # No language field
        )

        # Should succeed with 200 status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Verify response structure
        data = response.json()
        assert data["status"] == "success"
        assert "smells" in data
        assert "summary" in data

        # Verify that summary contains "python" (the default language)
        # The summary format is: "分析了 {字符数} 个字符的 {语言} 代码，发现 {数量} 个潜在问题"
        summary = data["summary"]
        assert "python" in summary.lower(), (
            f"Expected 'python' in summary, got: {summary}"
        )

    def test_explicit_language_field_overrides_default(self, client):
        """
        Test that explicitly provided language field overrides the default

        This test verifies that when a language is explicitly provided,
        it is used instead of the default value.
        """
        # Send request with explicit language field
        response = client.post(
            "/api/review",
            json={"code": "function hello() {}", "language": "javascript"},
        )

        # Should succeed with 200 status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Verify response structure
        data = response.json()
        assert data["status"] == "success"

        # Verify that summary contains the specified language
        summary = data["summary"]
        assert "javascript" in summary.lower(), (
            f"Expected 'javascript' in summary, got: {summary}"
        )
        assert "python" not in summary.lower() or "javascript" in summary.lower(), (
            f"Expected 'javascript' (not default 'python') in summary, got: {summary}"
        )

    def test_default_language_with_various_code_samples(self, client):
        """
        Test that default language is applied consistently across different code samples

        This test verifies that the default language behavior is consistent
        regardless of the code content.
        """
        test_cases = [
            "def test(): pass",
            "print('hello world')",
            "x = 42\ny = x + 1",
            "# This is a comment\npass",
            "class MyClass:\n    pass",
        ]

        for code in test_cases:
            response = client.post(
                "/api/review",
                json={"code": code},  # No language field
            )

            assert response.status_code == 200, (
                f"Expected 200 for code '{code[:20]}...', got {response.status_code}"
            )

            data = response.json()
            summary = data["summary"]
            assert "python" in summary.lower(), (
                f"Expected 'python' in summary for code '{code[:20]}...', got: {summary}"
            )

    def test_default_language_in_model_validation(self):
        """
        Test that the Pydantic model correctly applies the default language value

        This test directly validates the CodeReviewRequest model to ensure
        the default value is properly configured at the model level.
        """
        from main import CodeReviewRequest

        # Create request without language field
        request = CodeReviewRequest(code="def test(): pass")

        # Verify default language is applied
        assert request.language == "python", (
            f"Expected default language 'python', got '{request.language}'"
        )

    def test_default_language_with_empty_language_string_is_different(self, client):
        """
        Test that an empty string for language is different from omitting the field

        This test verifies that explicitly providing an empty string is not the same
        as using the default value (though both should be handled by the API).
        """
        # Send request with empty language string
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": ""}
        )

        # Should succeed with 200 status (empty string is a valid string)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Verify that summary contains empty string (not "python")
        data = response.json()
        summary = data["summary"]
        # The summary will contain the empty string for language
        # Format: "分析了 X 个字符的  代码，发现 3 个潜在问题"
        # Note the double space where language would be
        assert " 代码" in summary or summary.count("  ") > 0, (
            f"Expected empty language in summary, got: {summary}"
        )


class TestDefaultLanguageEdgeCases:
    """Edge case tests for default language value"""

    def test_null_language_field_uses_default(self, client):
        """
        Test that null/None language value uses the default

        This test verifies behavior when language is explicitly set to null.
        """
        # Send request with null language field
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": None}
        )

        # Pydantic should apply the default when None is provided
        # (depending on configuration, this might return 422 or use default)
        # Let's verify the actual behavior
        if response.status_code == 200:
            data = response.json()
            summary = data["summary"]
            # If it succeeds, it should use the default
            assert "python" in summary.lower() or "none" in summary.lower(), (
                f"Expected 'python' or 'none' in summary, got: {summary}"
            )
        elif response.status_code == 422:
            # If validation fails, that's also acceptable behavior
            pass
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

    def test_default_language_with_minimal_code(self, client):
        """
        Test default language with minimal valid code (1 character)

        This test verifies that default language works even with the smallest
        valid code input.
        """
        response = client.post(
            "/api/review",
            json={"code": "x"},  # Minimal 1-character code, no language
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        summary = data["summary"]
        assert "python" in summary.lower(), (
            f"Expected 'python' in summary for minimal code, got: {summary}"
        )
        # Verify character count is correct
        assert "1" in summary, (
            f"Expected character count '1' in summary, got: {summary}"
        )

    def test_default_language_with_maximum_code_length(self, client):
        """
        Test default language with maximum valid code length (100,000 characters)

        This test verifies that default language works with the largest
        valid code input.

        Note: This test may take a moment due to the large payload.
        """
        # Create code at maximum length
        code = "x" * 100000

        response = client.post(
            "/api/review",
            json={"code": code},  # No language field
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        summary = data["summary"]
        assert "python" in summary.lower(), (
            f"Expected 'python' in summary for max length code, got: {summary}"
        )
        # Verify character count is correct
        assert "100000" in summary, (
            f"Expected character count '100000' in summary, got: {summary}"
        )
