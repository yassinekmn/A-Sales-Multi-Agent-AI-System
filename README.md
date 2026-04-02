# 🤖 AI Data Team - Multi-Agent AI System

An autonomous multi-agent system that analyzes sales data, generates insights, and produces structured business reports using LLM-based agents.

## Architecture

```
User Query
    ↓
Planner Agent (decides workflow)
    ↓
Data Analyst Agent → Insight Generator → Report Writer
    ↓
Output to User
```

### **Agents**

- **Planner Agent**: Determines which agents to execute based on user request
- **Data Analyst Agent**: Analyzes sales data and answers questions
- **Insight Generator**: Generates actionable insights from analysis
- **Report Writer**: Creates professional business reports

## Features

✅ **Multi-Agent Orchestration** - Intelligent workflow planning  
✅ **Structured Logging** - Track all operations  
✅ **Input Validation** - Validate data and user inputs  
✅ **Error Handling** - Graceful failure management  
✅ **GitHub Marketplace LLM Integration** - Cost-effective API access  
✅ **Configuration Management** - Centralized environment config  
✅ **Type Hints** - Full type safety  
✅ **Unit Tests** - Comprehensive test coverage  

## Setup

### 1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Configure Environment**

Create a `.env` file with your GitHub Marketplace API tokens:

```env
# Planner Agent
PLANNER_GITHUB_TOKEN=ghp_your_token_here
PLANNER_GITHUB_MODEL=openai/gpt-4.1

# Data Analyst Agent
ANALYST_GITHUB_TOKEN=ghp_your_token_here
ANALYST_GITHUB_MODEL=openai/gpt-4.1

# Insight Generator
INSIGHT_GITHUB_TOKEN=ghp_your_token_here
INSIGHT_GITHUB_MODEL=openai/gpt-4.1

# Report Writer
REPORT_GITHUB_TOKEN=ghp_your_token_here
REPORT_GITHUB_MODEL=openai/gpt-4.1

# System Settings
GITHUB_ENDPOINT=https://models.github.ai/inference
DATA_FILE=sales.csv
LOG_LEVEL=INFO
```

### 3. **Run the System**

```bash
python main.py
```

## Usage Examples

### Analyze Data
```
📊 Ask your AI Data Team: Which region sold the most units?

📋 Planner decided: ANALYST
🔍 Data Analyst is analyzing...
```

### Generate Insights
```
📊 Ask your AI Data Team: Give me insights on sales performance

📋 Planner decided: ANALYST → INSIGHT
🔍 Data Analyst is analyzing...
💡 Insight Generator is processing...
```

### Create Full Report
```
📊 Ask your AI Data Team: Create  reporta comprehensive sales

📋 Planner decided: ANALYST → INSIGHT → REPORT
🔍 Data Analyst is analyzing...
💡 Insight Generator is processing...
📄 Report Writer is drafting...
```

## Project Structure

```
ai-agents-journey-new/
├── main.py                          # Entry point
├── config.py                        # Configuration management
├── data_analyst_agent.py            # Data analysis agent
├── planner_agent.py                 # Workflow planning agent
├── insight_generator_agent.py       # Insight generation agent
├── report_writer_agent.py           # Report writing agent
├── generate_data.py                 # Generates sample data
├── sales.csv                        # Sample dataset
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (git-ignored)
├── utils/
│   ├── __init__.py
│   ├── logger.py                    # Logging utilities
│   ├── errors.py                    # Custom exceptions
│   └── validators.py                # Input validation
└── tests/
    ├── test_validators.py           # Validator tests
    ├── test_planner.py              # Planner tests
    └── test_config.py               # Config tests
```

## Key Files

### **config.py**
Centralized configuration for all agents. Loads tokens and settings from environment variables.

### **utils/logger.py**
Structured logging with configuration from environment variables.

### **utils/errors.py**
Custom exception classes for different error scenarios:
- `AgentExecutionError` - Agent execution failures
- `DataValidationError` - Input validation failures  
- `LLMClientError` - LLM API failures

### **utils/validators.py**
Input validation functions:
- `validate_question()` - Validates user questions
- `validate_dataframe()` - Validates data structure
- `validate_llm_response()` - Validates LLM responses

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

## Error Handling

The system gracefully handles errors:

- **Missing Data**: Validates CSV before processing
- **Invalid Tokens**: Checks environment variables on startup
- **API Failures**: LLM calls have automatic retry logic
- **Bad Input**: User questions validated for length/content
- **Agent Failures**: Continues with other agents if one fails

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GITHUB_ENDPOINT` | `https://models.github.ai/inference` | GitHub Models API endpoint |
| `DATA_FILE` | `sales.csv` | Path to data file |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_RETRIES` | `3` | LLM call retry attempts |
| `TIMEOUT_SECONDS` | `30` | API call timeout |

## Logging

Logs include:
- Agent execution status
- Data validation results
- LLM API interactions
- Error stack traces (DEBUG level)

Example:
```
2026-04-03 00:39:10,120 - planner_agent - INFO - Planning tasks for: which region has the most sales?...
2026-04-03 00:39:13,119 - data_analyst_agent - INFO - Data Analyst starting...
2026-04-03 00:39:13,122 - data_analyst_agent - INFO - Data loaded: 200 rows
```

## Portfolio Highlights

This project demonstrates:

- **System Design**: Multi-agent orchestration with clear separation of concerns
- **Error Handling**: Comprehensive error management and recovery
- **Logging**: Structured logging for production monitoring
- **Testing**: Unit tests with mocking
- **Type Safety**: Full type hints throughout
- **Configuration Management**: Environment-driven configuration
- **LLM Integration**: Real GitHub Marketplace API integration
- **Code Quality**: Clean code, SOLID principles, DRY

## Future Enhancements

- [ ] Caching for identical queries
- [ ] Cost tracking per agent
- [ ] Async execution for parallel agents
- [ ] REST API endpoint
- [ ] Database persistence for reports
- [ ] User feedback loop for prompt optimization
- [ ] Support for additional data sources

## License

MIT
