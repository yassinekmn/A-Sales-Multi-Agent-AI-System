# insight_generator_agent.py
"""Insight Generator Agent - Generates insights from data analysis."""

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from config import AgentType, SystemConfig
from utils.logger import get_logger
from utils.validators import validate_llm_response
from utils.errors import AgentExecutionError

load_dotenv()

logger = get_logger(__name__)


def generate_insights(analyst_output: str) -> str:
    """
    Generate insights from data analysis.
    
    Args:
        analyst_output: Output from data analyst
        
    Returns:
        Insights response from LLM
        
    Raises:
        AgentExecutionError: If generation fails
    """
    try:
        if not analyst_output:
            raise ValueError("No analysis provided")
        
        logger.info("Insight Generator starting")
        
        # Get config
        agent_config = SystemConfig.get_agent_config(AgentType.INSIGHT)
        token = agent_config.get_token()
        model = agent_config.get_model()
        
        logger.debug(f"Using model: {model}")
        
        # Create client
        client = ChatCompletionsClient(
            endpoint=SystemConfig.ENDPOINT,
            credential=AzureKeyCredential(token),
        )
        
        prompt = f"""
Based on this analysis, generate actionable insights:

{analyst_output}

Focus on:
- Key trends and patterns
- Business implications
- Recommendations

Be clear and concise. Use bullet points.
"""
        
        response = client.complete(
            messages=[
                SystemMessage("You are an insights analyst."),
                UserMessage(prompt)
            ],
            model=model,
            temperature=1.0,
            top_p=1.0
        )
        
        result = response.choices[0].message.content
        validate_llm_response(result)
        
        logger.info("Insight generation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Insight generation failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("insight_generator", str(e), original_error=e)