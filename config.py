"""Configuration management for the multi-agent system."""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AgentType(Enum):
    """Available agent types in the system."""
    PLANNER = "planner"
    ANALYST = "analyst"
    INSIGHT = "insight"
    REPORT = "report"


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    name: str
    agent_type: AgentType
    token_env_var: str
    model_env_var: str
    system_prompt: str

    def get_token(self) -> str:
        """Retrieve API token from environment."""
        token = os.getenv(self.token_env_var)
        if not token:
            raise ValueError(f"Missing environment variable: {self.token_env_var}")
        return token

    def get_model(self) -> str:
        """Retrieve model name from environment."""
        model = os.getenv(self.model_env_var)
        if not model:
            raise ValueError(f"Missing environment variable: {self.model_env_var}")
        return model


class SystemConfig:
    """System-wide configuration."""
    
    ENDPOINT = os.getenv("GITHUB_ENDPOINT", "https://models.github.ai/inference")
    DATA_FILE = os.getenv("DATA_FILE", "sales.csv")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))

    # Agent configurations
    AGENTS = {
        AgentType.PLANNER: AgentConfig(
            name="Planner",
            agent_type=AgentType.PLANNER,
            token_env_var="PLANNER_GITHUB_TOKEN",
            model_env_var="PLANNER_GITHUB_MODEL",
            system_prompt="You are an AI planner for a data team."
        ),
        AgentType.ANALYST: AgentConfig(
            name="Data Analyst",
            agent_type=AgentType.ANALYST,
            token_env_var="ANALYST_GITHUB_TOKEN",
            model_env_var="ANALYST_GITHUB_MODEL",
            system_prompt="You are a data analyst."
        ),
        AgentType.INSIGHT: AgentConfig(
            name="Insight Generator",
            agent_type=AgentType.INSIGHT,
            token_env_var="INSIGHT_GITHUB_TOKEN",
            model_env_var="INSIGHT_GITHUB_MODEL",
            system_prompt="You generate insights from data."
        ),
        AgentType.REPORT: AgentConfig(
            name="Report Writer",
            agent_type=AgentType.REPORT,
            token_env_var="REPORT_GITHUB_TOKEN",
            model_env_var="REPORT_GITHUB_MODEL",
            system_prompt="You write professional business reports."
        ),
    }

    @classmethod
    def get_agent_config(cls, agent_type: AgentType) -> AgentConfig:
        """Get configuration for a specific agent."""
        if agent_type not in cls.AGENTS:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls.AGENTS[agent_type]
