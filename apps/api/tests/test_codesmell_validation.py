"""
Tests for CodeSmell model validation constraints

This test file verifies that the CodeSmell model enforces all validation rules:
- type field: minimum length of 3 characters
- severity field: enum validation (low, medium, high)
- line field: positive integer (> 0)
- message field: minimum length of 5 characters
- suggestion field: minimum length of 10 characters

Validates Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
"""

import pytest
from pydantic import ValidationError
from main import CodeSmell


class TestCodeSmellTypeValidation:
    """Tests for CodeSmell.type field validation"""

    def test_type_with_valid_length(self):
        """Test that type with >= 3 characters is accepted"""
        smell = CodeSmell(
            type="Long Method",
            severity="medium",
            line=10,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.type == "Long Method"

    def test_type_with_minimum_length(self):
        """Test that type with exactly 3 characters is accepted"""
        smell = CodeSmell(
            type="ABC",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.type == "ABC"

    def test_type_too_short_raises_validation_error(self):
        """Test that type with < 3 characters is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="AB",  # Only 2 characters
                severity="low",
                line=1,
                message="Test message",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("type",) for error in errors)

    def test_type_empty_string_raises_validation_error(self):
        """Test that empty type string is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="",
                severity="low",
                line=1,
                message="Test message",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("type",) for error in errors)


class TestCodeSmellSeverityValidation:
    """Tests for CodeSmell.severity field validation"""

    def test_severity_low_is_accepted(self):
        """Test that severity='low' is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.severity == "low"

    def test_severity_medium_is_accepted(self):
        """Test that severity='medium' is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="medium",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.severity == "medium"

    def test_severity_high_is_accepted(self):
        """Test that severity='high' is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="high",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.severity == "high"

    def test_severity_invalid_value_raises_validation_error(self):
        """Test that invalid severity value is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="critical",  # Invalid value
                line=1,
                message="Test message",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("severity",) for error in errors)

    def test_severity_empty_string_raises_validation_error(self):
        """Test that empty severity string is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="",
                line=1,
                message="Test message",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("severity",) for error in errors)


class TestCodeSmellLineValidation:
    """Tests for CodeSmell.line field validation"""

    def test_line_positive_integer_is_accepted(self):
        """Test that positive line number is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=42,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.line == 42

    def test_line_minimum_value_one_is_accepted(self):
        """Test that line=1 is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        assert smell.line == 1

    def test_line_zero_raises_validation_error(self):
        """Test that line=0 is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="low",
                line=0,
                message="Test message",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("line",) for error in errors)

    def test_line_negative_raises_validation_error(self):
        """Test that negative line number is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="low",
                line=-5,
                message="Test message",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("line",) for error in errors)


class TestCodeSmellMessageValidation:
    """Tests for CodeSmell.message field validation"""

    def test_message_with_valid_length(self):
        """Test that message with >= 5 characters is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="This is a valid message",
            suggestion="Test suggestion here",
        )
        assert smell.message == "This is a valid message"

    def test_message_with_minimum_length(self):
        """Test that message with exactly 5 characters is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="12345",
            suggestion="Test suggestion here",
        )
        assert smell.message == "12345"

    def test_message_too_short_raises_validation_error(self):
        """Test that message with < 5 characters is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="low",
                line=1,
                message="1234",  # Only 4 characters
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("message",) for error in errors)

    def test_message_empty_string_raises_validation_error(self):
        """Test that empty message string is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="low",
                line=1,
                message="",
                suggestion="Test suggestion here",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("message",) for error in errors)


class TestCodeSmellSuggestionValidation:
    """Tests for CodeSmell.suggestion field validation"""

    def test_suggestion_with_valid_length(self):
        """Test that suggestion with >= 10 characters is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="This is a valid suggestion with enough characters",
        )
        assert smell.suggestion == "This is a valid suggestion with enough characters"

    def test_suggestion_with_minimum_length(self):
        """Test that suggestion with exactly 10 characters is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="1234567890",
        )
        assert smell.suggestion == "1234567890"

    def test_suggestion_too_short_raises_validation_error(self):
        """Test that suggestion with < 10 characters is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="low",
                line=1,
                message="Test message",
                suggestion="123456789",  # Only 9 characters
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("suggestion",) for error in errors)

    def test_suggestion_empty_string_raises_validation_error(self):
        """Test that empty suggestion string is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeSmell(
                type="Test Type",
                severity="low",
                line=1,
                message="Test message",
                suggestion="",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("suggestion",) for error in errors)


class TestCodeSmellIntegration:
    """Integration tests for CodeSmell model with API endpoint"""

    def test_api_returns_valid_codesmells(self, client):
        """Test that API endpoint returns CodeSmells that pass all validation"""
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()

        # Verify all returned smells meet validation constraints
        for smell in data["smells"]:
            assert len(smell["type"]) >= 3
            assert smell["severity"] in ["low", "medium", "high"]
            assert smell["line"] > 0
            assert len(smell["message"]) >= 5
            assert len(smell["suggestion"]) >= 10
