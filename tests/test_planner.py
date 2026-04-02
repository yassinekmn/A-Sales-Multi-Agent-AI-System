"""Unit tests for planner agent."""

import pytest
import json
from unittest.mock import patch, MagicMock
from planner_agent import plan_tasks


class TestPlannerAgent:
    """Test planner agent functionality."""

    @patch('planner_agent.ChatCompletionsClient')
    @patch('planner_agent.AzureKeyCredential')
    @patch.dict('os.environ', {
        'PLANNER_GITHUB_TOKEN': 'test_token',
        'PLANNER_GITHUB_MODEL': 'gpt-4.1'
    })
    def test_plan_tasks_analyst_only(self, mock_credential, mock_client_class):
        """Test planner returns analyst for data question."""
        # Mock the API response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = '["analyst"]'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.complete.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        result = plan_tasks("Which region has the most sales?")
        
        assert result == ["analyst"]
        mock_client.complete.assert_called_once()

    @patch('planner_agent.ChatCompletionsClient')
    @patch('planner_agent.AzureKeyCredential')
    @patch.dict('os.environ', {
        'PLANNER_GITHUB_TOKEN': 'test_token',
        'PLANNER_GITHUB_MODEL': 'gpt-4.1'
    })
    def test_plan_tasks_full_workflow(self, mock_credential, mock_client_class):
        """Test planner returns full workflow."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = '["analyst", "insight", "report"]'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.complete.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        result = plan_tasks("Create a comprehensive sales report")
        
        assert result == ["analyst", "insight", "report"]

    @patch('planner_agent.ChatCompletionsClient')
    @patch('planner_agent.AzureKeyCredential')
    @patch.dict('os.environ', {
        'PLANNER_GITHUB_TOKEN': 'test_token',
        'PLANNER_GITHUB_MODEL': 'gpt-4.1'
    })
    def test_plan_tasks_invalid_json(self, mock_credential, mock_client_class):
        """Test planner falls back on invalid JSON."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        # Invalid JSON response
        mock_message.content = 'This is not JSON'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.complete.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        result = plan_tasks("Some question")
        
        # Should return default workflow
        assert result == ["analyst", "insight", "report"]

    @patch('planner_agent.ChatCompletionsClient')
    @patch('planner_agent.AzureKeyCredential')
    @patch.dict('os.environ', {
        'PLANNER_GITHUB_TOKEN': 'test_token',
        'PLANNER_GITHUB_MODEL': 'gpt-4.1'
    })
    def test_plan_tasks_empty_array(self, mock_credential, mock_client_class):
        """Test planner handles empty array response."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = '[]'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.complete.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        result = plan_tasks("Some question")
        
        # Empty array is returned as-is (edge case)
        assert result == []

    def test_plan_tasks_missing_token(self):
        """Test planner raises error with missing token."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(Exception):  # Should raise about missing token
                plan_tasks("Some question")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
