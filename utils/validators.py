"""Input validation utilities."""

import pandas as pd
from utils.errors import DataValidationError


def validate_question(question: str, min_length: int = 3) -> None:
    """Validate user question."""
    if not question or len(question.strip()) < min_length:
        raise DataValidationError(f"Question must be at least {min_length} characters")


def validate_dataframe(df: pd.DataFrame, required_columns=None) -> None:
    """Validate dataframe structure."""
    if df is None or df.empty:
        raise DataValidationError("DataFrame is empty")
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise DataValidationError(f"Missing columns: {missing}")


def validate_llm_response(response: str, min_length: int = 10) -> None:
    """Validate LLM response."""
    if not response or len(response.strip()) < min_length:
        raise DataValidationError(f"LLM response too short (minimum {min_length} chars)")
