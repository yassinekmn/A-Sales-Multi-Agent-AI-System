"""Custom exception classes for the multi-agent system."""


class AgentExecutionError(Exception):
    """Raised when an agent fails to execute."""
    def __init__(self, agent_name: str, message: str, original_error=None):
        self.agent_name = agent_name
        self.message = message
        self.original_error = original_error
        super().__init__(f"[{agent_name}] {message}")


class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass


class LLMClientError(Exception):
    """Raised when LLM client operations fail."""
    pass
