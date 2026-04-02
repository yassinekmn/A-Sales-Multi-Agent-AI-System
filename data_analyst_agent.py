# data_analyst_agent.py
"""Data Analyst Agent - Analyzes sales data and answers questions."""

import os
import pandas as pd
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from config import AgentType, SystemConfig
from utils.logger import get_logger
from utils.validators import validate_question, validate_dataframe, validate_llm_response
from utils.errors import AgentExecutionError, DataValidationError

load_dotenv()

logger = get_logger(__name__)


def analyze_data(user_question: str) -> str:
    """
    Analyze sales data and answer user question.
    
    Args:
        user_question: The question to answer
        
    Returns:
        Analysis response from LLM
        
    Raises:
        DataValidationError: If input validation fails
        AgentExecutionError: If analysis fails
    """
    try:
        logger.info(f"Data Analyst starting. Question: {user_question[:50]}...")
        
        # Validate input
        validate_question(user_question)
        
        # Load and validate data
        df = pd.read_csv(SystemConfig.DATA_FILE)
        validate_dataframe(df, required_columns=["Date", "Product", "Region", "Sales", "Quantity"])
        logger.info(f"Data loaded: {len(df)} rows")
        
        # Compute summary
        summary = {
            "total_rows": len(df),
            "regions": df["Region"].unique().tolist(),
            "products": df["Product"].unique().tolist(),
            "total_sales": float(df["Sales"].sum()),
            "total_quantity": int(df["Quantity"].sum()),
            "sales_by_region": df.groupby("Region")["Sales"].sum().to_dict(),
            "quantity_by_region": df.groupby("Region")["Quantity"].sum().to_dict(),
            "sales_by_product": df.groupby("Product")["Sales"].sum().to_dict(),
        }
        
        # Get agent config
        agent_config = SystemConfig.get_agent_config(AgentType.ANALYST)
        token = agent_config.get_token()
        model = agent_config.get_model()
        
        logger.debug(f"Using model: {model}")
        
        # Create client and call API
        client = ChatCompletionsClient(
            endpoint=SystemConfig.ENDPOINT,
            credential=AzureKeyCredential(token),
        )
        
        prompt = f"""
You are a data analyst. Analyze the following data and answer the user's question:

Data Summary:
{summary}

User Question: {user_question}

Provide a clear, concise analysis based on the data.
"""
        
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful data analyst."),
                UserMessage(prompt)
            ],
            model=model,
            temperature=1.0,
            top_p=1.0
        )
        
        result = response.choices[0].message.content
        validate_llm_response(result)
        
        logger.info("Data analysis completed successfully")
        return result
        
    except DataValidationError as e:
        logger.error(f"Data validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Data analysis failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("data_analyst", str(e), original_error=e)