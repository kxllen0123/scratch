"""
Tests for CodeReviewResponse model validation constraints

This test file verifies that the CodeReviewResponse model enforces all validation rules:
- smells field: minimum list length of 1
- summary field: minimum length of 10 characters

Validates Requirements: 4.3, 4.4
"""

import pytest
from pydantic import ValidationError
from main import CodeReviewResponse, CodeSmell


class TestCodeReviewResponseSmellsValidation:
    """Tests for CodeReviewResponse.smells field validation"""

    def test_smells_with_one_element_is_accepted(self):
        """Test that smells list with 1 element is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        response = CodeReviewResponse(
            status="success",
            smells=[smell],
            summary="This is a valid summary with enough characters",
        )
        assert len(response.smells) == 1

    def test_smells_with_multiple_elements_is_accepted(self):
        """Test that smells list with multiple elements is accepted"""
        smell1 = CodeSmell(
            type="Test Type 1",
            severity="low",
            line=1,
            message="Test message 1",
            suggestion="Test suggestion here 1",
        )
        smell2 = CodeSmell(
            type="Test Type 2",
            severity="medium",
            line=2,
            message="Test message 2",
            suggestion="Test suggestion here 2",
        )
        smell3 = CodeSmell(
            type="Test Type 3",
            severity="high",
            line=3,
            message="Test message 3",
            suggestion="Test suggestion here 3",
        )
        response = CodeReviewResponse(
            status="success",
            smells=[smell1, smell2, smell3],
            summary="This is a valid summary with enough characters",
        )
        assert len(response.smells) == 3

    def test_smells_empty_list_raises_validation_error(self):
        """Test that empty smells list is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CodeReviewResponse(
                status="success",
                smells=[],  # Empty list
                summary="This is a valid summary with enough characters",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("smells",) for error in errors)
        assert any(
            "at least 1" in str(error["msg"]).lower()
            or "min_length" in str(error["type"]).lower()
            for error in errors
        )


class TestCodeReviewResponseSummaryValidation:
    """Tests for CodeReviewResponse.summary field validation"""

    def test_summary_with_valid_length(self):
        """Test that summary with >= 10 characters is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        response = CodeReviewResponse(
            status="success",
            smells=[smell],
            summary="This is a valid summary with more than enough characters",
        )
        assert (
            response.summary
            == "This is a valid summary with more than enough characters"
        )

    def test_summary_with_minimum_length(self):
        """Test that summary with exactly 10 characters is accepted"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        response = CodeReviewResponse(
            status="success",
            smells=[smell],
            summary="1234567890",  # Exactly 10 characters
        )
        assert response.summary == "1234567890"

    def test_summary_too_short_raises_validation_error(self):
        """Test that summary with < 10 characters is rejected"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        with pytest.raises(ValidationError) as exc_info:
            CodeReviewResponse(
                status="success",
                smells=[smell],
                summary="123456789",  # Only 9 characters
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("summary",) for error in errors)

    def test_summary_empty_string_raises_validation_error(self):
        """Test that empty summary string is rejected"""
        smell = CodeSmell(
            type="Test Type",
            severity="low",
            line=1,
            message="Test message",
            suggestion="Test suggestion here",
        )
        with pytest.raises(ValidationError) as exc_info:
            CodeReviewResponse(status="success", smells=[smell], summary="")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("summary",) for error in errors)


class TestCodeReviewResponseIntegration:
    """Integration tests for CodeReviewResponse model with API endpoint"""

    def test_api_returns_valid_response_structure(self, client):
        """Test that API endpoint returns CodeReviewResponse that passes all validation"""
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()

        # Verify response meets validation constraints
        assert data["status"] == "success"
        assert len(data["smells"]) >= 1  # At least 1 smell
        assert len(data["summary"]) >= 10  # Summary at least 10 characters

    def test_api_returns_exactly_three_smells(self, client):
        """Test that API returns exactly 3 smells as per requirements"""
        response = client.post(
            "/api/review", json={"code": "def test(): pass", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()

        # Verify exactly 3 smells (Requirement 4.5)
        assert len(data["smells"]) == 3

    def test_api_summary_contains_required_information(self, client):
        """Test that API summary contains character count, language, and smell count"""
        test_code = "def hello(): pass"
        response = client.post(
            "/api/review", json={"code": test_code, "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()

        # Verify summary contains required information (Requirements 6.4, 6.5, 6.6)
        summary = data["summary"]
        assert str(len(test_code)) in summary  # Character count
        assert "python" in summary.lower()  # Language name
        assert "3" in summary  # Smell count
