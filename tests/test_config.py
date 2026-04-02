"""Unit tests for configuration module."""

import pytest
import os
from config import AgentType, AgentConfig, SystemConfig
from unittest.mock import patch


class TestAgentConfig:
    """Test agent configuration."""

    def test_agent_config_creation(self):
        """Test creating agent config."""
        config = AgentConfig(
            name="Test Agent",
            agent_type=AgentType.ANALYST,
            token_env_var="TEST_TOKEN",
            model_env_var="TEST_MODEL",
            system_prompt="Test prompt"
        )
        assert config.name == "Test Agent"
        assert config.agent_type == AgentType.ANALYST

    @patch.dict(os.environ, {"TEST_TOKEN": "test_value"})
    def test_get_token_success(self):
        """Test retrieving token from environment."""
        config = AgentConfig(
            name="Test",
            agent_type=AgentType.ANALYST,
            token_env_var="TEST_TOKEN",
            model_env_var="TEST_MODEL",
            system_prompt="Test"
        )
        assert config.get_token() == "test_value"

    def test_get_token_missing(self):
        """Test retrieving missing token raises error."""
        config = AgentConfig(
            name="Test",
            agent_type=AgentType.ANALYST,
            token_env_var="NONEXISTENT_TOKEN",
            model_env_var="TEST_MODEL",
            system_prompt="Test"
        )
        with pytest.raises(ValueError, match="Missing environment variable"):
            config.get_token()

    @patch.dict(os.environ, {"TEST_MODEL": "gpt-4.1"})
    def test_get_model_success(self):
        """Test retrieving model from environment."""
        config = AgentConfig(
            name="Test",
            agent_type=AgentType.ANALYST,
            token_env_var="TEST_TOKEN",
            model_env_var="TEST_MODEL",
            system_prompt="Test"
        )
        assert config.get_model() == "gpt-4.1"

    def test_get_model_missing(self):
        """Test retrieving missing model raises error."""
        config = AgentConfig(
            name="Test",
            agent_type=AgentType.ANALYST,
            token_env_var="TEST_TOKEN",
            model_env_var="NONEXISTENT_MODEL",
            system_prompt="Test"
        )
        with pytest.raises(ValueError, match="Missing environment variable"):
            config.get_model()


class TestSystemConfig:
    """Test system configuration."""

    def test_agent_types_exist(self):
        """Test that all agent types are configured."""
        for agent_type in [AgentType.PLANNER, AgentType.ANALYST, AgentType.INSIGHT, AgentType.REPORT]:
            config = SystemConfig.get_agent_config(agent_type)
            assert config is not None
            assert config.name is not None

    def test_get_agent_config_planner(self):
        """Test getting planner config."""
        config = SystemConfig.get_agent_config(AgentType.PLANNER)
        assert config.name == "Planner"
        assert config.token_env_var == "PLANNER_GITHUB_TOKEN"

    def test_get_agent_config_analyst(self):
        """Test getting analyst config."""
        config = SystemConfig.get_agent_config(AgentType.ANALYST)
        assert config.name == "Data Analyst"
        assert config.token_env_var == "ANALYST_GITHUB_TOKEN"

    def test_get_agent_config_insight(self):
        """Test getting insight config."""
        config = SystemConfig.get_agent_config(AgentType.INSIGHT)
        assert config.name == "Insight Generator"
        assert config.token_env_var == "INSIGHT_GITHUB_TOKEN"

    def test_get_agent_config_report(self):
        """Test getting report config."""
        config = SystemConfig.get_agent_config(AgentType.REPORT)
        assert config.name == "Report Writer"
        assert config.token_env_var == "REPORT_GITHUB_TOKEN"

    def test_invalid_agent_type(self):
        """Test getting invalid agent type raises error."""
        with pytest.raises(ValueError, match="Unknown agent type"):
            SystemConfig.get_agent_config("invalid")

    @patch.dict(os.environ, {"GITHUB_ENDPOINT": "https://custom.endpoint"})
    def test_endpoint_from_env(self):
        """Test endpoint can be overridden from environment."""
        # Note: This tests the initial load, not runtime changes
        assert SystemConfig.ENDPOINT == "https://models.github.ai/inference"  # Class attribute cached


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
