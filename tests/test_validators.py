"""Unit tests for validators module."""

import pytest
import pandas as pd
from utils.validators import validate_question, validate_dataframe, validate_llm_response
from utils.errors import DataValidationError


class TestValidators:
    """Test input validators."""

    def test_validate_question_valid(self):
        """Test validation of valid questions."""
        validate_question("What is the sales trend?")
        validate_question("Show me data")
        # Should not raise

    def test_validate_question_empty(self):
        """Test validation of empty question."""
        with pytest.raises(DataValidationError):
            validate_question("")

    def test_validate_question_too_short(self):
        """Test validation of short question."""
        with pytest.raises(DataValidationError):
            validate_question("ab")

    def test_validate_question_none(self):
        """Test validation of None question."""
        with pytest.raises(DataValidationError):
            validate_question(None)

    def test_validate_dataframe_valid(self):
        """Test validation of valid dataframe."""
        df = pd.DataFrame({
            'Date': ['2025-01-01'],
            'Product': ['Laptop'],
            'Region': ['North'],
            'Sales': [1000],
            'Quantity': [1]
        })
        validate_dataframe(df, required_columns=['Date', 'Product', 'Region', 'Sales', 'Quantity'])
        # Should not raise

    def test_validate_dataframe_empty(self):
        """Test validation of empty dataframe."""
        df = pd.DataFrame()
        with pytest.raises(DataValidationError):
            validate_dataframe(df)

    def test_validate_dataframe_missing_columns(self):
        """Test validation of dataframe with missing columns."""
        df = pd.DataFrame({'Date': ['2025-01-01']})
        with pytest.raises(DataValidationError):
            validate_dataframe(df, required_columns=['Date', 'Product'])

    def test_validate_llm_response_valid(self):
        """Test validation of valid LLM response."""
        validate_llm_response("This is a valid response with enough characters.")
        # Should not raise

    def test_validate_llm_response_too_short(self):
        """Test validation of short LLM response."""
        with pytest.raises(DataValidationError):
            validate_llm_response("Short")

    def test_validate_llm_response_empty(self):
        """Test validation of empty LLM response."""
        with pytest.raises(DataValidationError):
            validate_llm_response("")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
