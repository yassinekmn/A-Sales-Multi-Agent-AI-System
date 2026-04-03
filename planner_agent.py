# planner_agent.py
"""Planner Agent - Determines which agents to execute."""

import os
import json
from typing import List
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from config import AgentType, SystemConfig
from utils.logger import get_logger
from utils.errors import AgentExecutionError

load_dotenv()

logger = get_logger(__name__)


def plan_tasks(user_input: str) -> List[str]:
    """
    Determine which agents should execute.
    
    Args:
        user_input: User's request
        
    Returns:
        List of agent names to execute
        
    Raises:
        AgentExecutionError: If planning fails
    """
    try:
        logger.info(f"Planning tasks for: {user_input[:50]}...")
        
        # Get config
        agent_config = SystemConfig.get_agent_config(AgentType.PLANNER)
        token = agent_config.get_token()
        model = agent_config.get_model()
        
        logger.debug(f"Using model: {model}")
        
        # Create client
        client = ChatCompletionsClient(
            endpoint=SystemConfig.ENDPOINT,
            credential=AzureKeyCredential(token),
        )
        
        prompt = f"""
You are an AI planner for a data team.

Available agents:
- analyst → analyzes data and answers questions
- insight → generates insights from analysis
- report → writes business reports
- comparison → compares sales across regions/products
- export → exports reports in PDF, Excel, JSON, HTML formats

Return ONLY a valid JSON array of agent names.

Examples:
- "Which region sold most?" → ["analyst"]
- "Give me insights" → ["analyst", "insight"]
- "Create a report" → ["analyst", "insight", "report"]
- "Compare north and south regions" → ["comparison"]
- "Export the analysis as PDF" → ["analyst", "export"]

User: {user_input}

Return ONLY the JSON array, nothing else:
"""
        
        response = client.complete(
            messages=[
                SystemMessage("You are a planning assistant."),
                UserMessage(prompt)
            ],
            model=model,
            temperature=1.0,
            top_p=1.0
        )
        
        response_text = response.choices[0].message.content.strip()
        logger.debug(f"Planner response: {response_text}")
        
        try:
            steps = json.loads(response_text)
            if isinstance(steps, list):
                logger.info(f"Planner decided: {steps}")
                return steps
        except json.JSONDecodeError:
            logger.warning("Failed to parse planner JSON, using default")
        
        # Fallback
        logger.warning("Using default workflow: analyst → insight → report")
        return ["analyst", "insight", "report"]
        
    except Exception as e:
        logger.error(f"Planning failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("planner", str(e), original_error=e)