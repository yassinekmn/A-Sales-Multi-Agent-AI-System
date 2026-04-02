# report_writer_agent.py
"""Report Writer Agent - Generates structured business reports."""

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


def generate_report(user_question: str, analyst_output: str, insights: str) -> str:
    """
    Generate a structured business report.
    
    Args:
        user_question: Original user question
        analyst_output: Output from data analyst
        insights: Output from insight generator
        
    Returns:
        Report response from LLM
        
    Raises:
        AgentExecutionError: If generation fails
    """
    try:
        if not analyst_output or not insights:
            raise ValueError("Missing analysis or insights data")
        
        logger.info("Report Writer starting")
        
        # Get config
        agent_config = SystemConfig.get_agent_config(AgentType.REPORT)
        token = agent_config.get_token()
        model = agent_config.get_model()
        
        logger.debug(f"Using model: {model}")
        
        # Create client
        client = ChatCompletionsClient(
            endpoint=SystemConfig.ENDPOINT,
            credential=AzureKeyCredential(token),
        )
        
        prompt = f"""
Write a professional executive report based on:

User Request: {user_question}

Analysis:
{analyst_output}

Insights:
{insights}

Include:
1. Title
2. Executive Summary
3. Key Findings
4. Analysis & Recommendations
5. Conclusion

Be professional and clear. Use section headers.
"""
        
        response = client.complete(
            messages=[
                SystemMessage("You are a professional report writer."),
                UserMessage(prompt)
            ],
            model=model,
            temperature=1.0,
            top_p=1.0
        )
        
        result = response.choices[0].message.content
        validate_llm_response(result)
        
        logger.info("Report generation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("report_writer", str(e), original_error=e)