# comparison_agent.py
"""Comparison Agent - Compares sales across different dimensions (regions, products, time)."""

import os
import pandas as pd
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from config import AgentType, SystemConfig
from utils.logger import get_logger
from utils.errors import AgentExecutionError, DataValidationError

load_dotenv()

logger = get_logger(__name__)


def compare_regions(metric: str = "sales") -> str:
    """
    Compare sales across regions.
    
    Args:
        metric: 'sales' or 'quantity'
        
    Returns:
        Comparison analysis from LLM
        
    Raises:
        AgentExecutionError: If comparison fails
    """
    try:
        logger.info(f"Comparing regions by {metric}")
        
        # Load data
        df = pd.read_csv(SystemConfig.DATA_FILE)
        
        # Aggregate by region
        if metric.lower() == "sales":
            comparison = df.groupby("Region")["Sales"].agg(['sum', 'mean', 'count']).round(2)
        elif metric.lower() == "quantity":
            comparison = df.groupby("Region")["Quantity"].agg(['sum', 'mean', 'count']).round(2)
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        # Get LLM analysis
        return _get_comparison_analysis(
            comparison_data=comparison.to_string(),
            comparison_type="regions",
            metric=metric
        )
        
    except Exception as e:
        logger.error(f"Region comparison failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("comparison_agent", str(e), original_error=e)


def compare_products(metric: str = "sales") -> str:
    """
    Compare sales across products.
    
    Args:
        metric: 'sales' or 'quantity'
        
    Returns:
        Comparison analysis from LLM
        
    Raises:
        AgentExecutionError: If comparison fails
    """
    try:
        logger.info(f"Comparing products by {metric}")
        
        # Load data
        df = pd.read_csv(SystemConfig.DATA_FILE)
        
        # Aggregate by product
        if metric.lower() == "sales":
            comparison = df.groupby("Product")["Sales"].agg(['sum', 'mean', 'count']).round(2)
        elif metric.lower() == "quantity":
            comparison = df.groupby("Product")["Quantity"].agg(['sum', 'mean', 'count']).round(2)
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        # Get LLM analysis
        return _get_comparison_analysis(
            comparison_data=comparison.to_string(),
            comparison_type="products",
            metric=metric
        )
        
    except Exception as e:
        logger.error(f"Product comparison failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("comparison_agent", str(e), original_error=e)


def compare_head_to_head(dimension: str, item1: str, item2: str, metric: str = "sales") -> str:
    """
    Compare two specific items head-to-head.
    
    Args:
        dimension: 'region' or 'product'
        item1: First item to compare
        item2: Second item to compare
        metric: 'sales' or 'quantity'
        
    Returns:
        Head-to-head comparison analysis
        
    Raises:
        AgentExecutionError: If comparison fails
    """
    try:
        dimension = dimension.lower()
        if dimension not in ['region', 'product']:
            raise ValueError("Dimension must be 'region' or 'product'")
        
        logger.info(f"Comparing {item1} vs {item2} ({dimension})")
        
        # Load data
        df = pd.read_csv(SystemConfig.DATA_FILE)
        
        # Filter data for both items
        col_name = dimension.capitalize()
        data1 = df[df[col_name] == item1]
        data2 = df[df[col_name] == item2]
        
        if data1.empty or data2.empty:
            raise DataValidationError(f"No data found for {item1} or {item2}")
        
        # Prepare comparison
        comparison_dict = {
            item1: {
                f"Total {metric}": data1[metric.capitalize()].sum(),
                "Average": data1[metric.capitalize()].mean(),
                "Count": len(data1)
            },
            item2: {
                f"Total {metric}": data2[metric.capitalize()].sum(),
                "Average": data2[metric.capitalize()].mean(),
                "Count": len(data2)
            }
        }
        
        # Get LLM analysis
        return _get_comparison_analysis(
            comparison_data=str(comparison_dict),
            comparison_type=f"{item1} vs {item2}",
            metric=metric
        )
        
    except Exception as e:
        logger.error(f"Head-to-head comparison failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("comparison_agent", str(e), original_error=e)


def _get_comparison_analysis(comparison_data: str, comparison_type: str, metric: str) -> str:
    """
    Get LLM analysis of comparison data.
    
    Args:
        comparison_data: Formatted comparison data
        comparison_type: Type of comparison
        metric: Metric being compared
        
    Returns:
        LLM analysis
    """
    try:
        # Use ANALYST token (reusing existing token)
        agent_config = SystemConfig.get_agent_config(AgentType.ANALYST)
        token = agent_config.get_token()
        model = agent_config.get_model()
        
        logger.debug(f"Using model: {model}")
        
        client = ChatCompletionsClient(
            endpoint=SystemConfig.ENDPOINT,
            credential=AzureKeyCredential(token),
        )
        
        prompt = f"""
Analyze the following comparison data and provide insights:

Comparison Type: {comparison_type}
Metric: {metric}

Data:
{comparison_data}

Provide:
1. Key findings (which is performing better and why)
2. Percentage differences where applicable
3. Recommendations based on the comparison
4. Any concerning trends

Be concise and data-driven.
"""
        
        response = client.complete(
            messages=[
                SystemMessage("You are an expert data analyst specializing in comparative analysis."),
                UserMessage(prompt)
            ],
            model=model,
            temperature=1.0,
            top_p=1.0
        )
        
        result = response.choices[0].message.content
        logger.info("Comparison analysis completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"LLM comparison analysis failed: {str(e)}", exc_info=True)
        raise AgentExecutionError("comparison_agent", str(e), original_error=e)
