# 🤖 AI Data Team - Multi-Agent AI System

An autonomous multi-agent system that analyzes sales data, generates insights, and produces structured business reports using LLM-based agents.

## Architecture

```
User Query
    ↓
Planner Agent (decides workflow)
    ↓
┌─────────────────────────────────────────┐
│  Data Analyst  │  Comparison  │ Export │
│     Agent      │    Agent     │ Agent  │
└─────────────────────────────────────────┘
    ↓
 Insight Generator → Report Writer
    ↓
Output to User
```

### **Agents**

- **Planner Agent**: Determines which agents to execute based on user request
- **Data Analyst Agent**: Analyzes sales data and answers business questions
- **Comparison Agent**: Compares metrics across regions or products
- **Insight Generator**: Generates actionable insights from analysis
- **Report Writer**: Creates professional business reports
- **Export Agent**: Exports reports in multiple formats (JSON, TXT, HTML, PDF)

## Features

✅ **Multi-Agent Orchestration** - Intelligent workflow planning with 6 specialized agents  
✅ **Comparative Analysis** - Compare regions, products, and performance metrics  
✅ **Multi-Format Export** - JSON, TXT, HTML, PDF report generation  
✅ **Structured Logging** - Track all operations with configurable levels  
✅ **Input Validation** - Validate data and user inputs  
✅ **Error Handling** - Graceful failure management with custom exceptions  
✅ **GitHub Marketplace LLM Integration** - Cost-effective API access with token reuse  
✅ **Configuration Management** - Centralized environment config  
✅ **Type Hints** - Full type safety throughout codebase  
✅ **Unit Tests** - Comprehensive test coverage (27 tests)  

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
📊 Ask your AI Data Team: Create a comprehensive sales report

📋 Planner decided: ANALYST → INSIGHT → REPORT
🔍 Data Analyst is analyzing...
💡 Insight Generator is processing...
📄 Report Writer is drafting...
```

### Compare Regions
```
📊 Ask your AI Data Team: Compare sales across regions

📋 Planner decided: COMPARISON
📊 Comparison Agent is analyzing...
```

### Export Analysis
```
📊 Ask your AI Data Team: Export this as PDF

📋 Planner decided: ANALYST → EXPORT
💾 Export Agent is preparing...
✓ Report exported to: exports/report_20260403_014207.pdf
```

## Project Structure

```
ai-agents-journey-new/
├── main.py                          # Entry point & orchestration loop
├── config.py                        # Configuration management
├── data_analyst_agent.py            # Data analysis agent
├── planner_agent.py                 # Workflow planning agent
├── insight_generator_agent.py       # Insight generation agent
├── report_writer_agent.py           # Report writing agent
├── comparison_agent.py              # Regional/product comparison agent
├── export_agent.py                  # Multi-format export agent
├── generate_data.py                 # Generates sample data
├── sales.csv                        # Sample dataset
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (git-ignored)
├── .gitignore                       # Git exclusions (exports/)
├── utils/
│   ├── __init__.py
│   ├── logger.py                    # Logging utilities
│   ├── errors.py                    # Custom exceptions
│   └── validators.py                # Input validation
├── tests/
│   ├── test_validators.py           # Validator tests
│   ├── test_planner.py              # Planner tests
│   └── test_config.py               # Config tests
└── exports/                         # Generated reports (git-ignored)
    ├── report_20260403_014207.json
    ├── report_20260403_014207.html
    └── report_20260403_014207.pdf
```

## Key Files

### **config.py**
Centralized configuration for all 6 agents. Loads tokens and settings from environment variables.
- Defines `AgentType` enum with PLANNER, ANALYST, INSIGHT, REPORT, COMPARISON, EXPORT
- Maps each agent to configuration (token, model, base URL)
- Supports token reuse (Comparison and Export agents share ANALYST token)

### **comparison_agent.py**
Performs comparative analysis across business dimensions:
- `compare_regions()` - Compare sales metrics by region
- `compare_products()` - Compare products by key metrics
- `compare_head_to_head()` - Direct comparison of two entities

### **export_agent.py**
Exports reports in multiple formats:
- `export_report()` - Main export function supporting JSON, TXT, HTML, PDF
- Generates timestamped files in `exports/` directory
- Includes metadata (format, timestamp, size)

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

- **System Design**: 6-agent architecture with intelligent workflow orchestration
- **Agent Specialization**: Each agent has a specific, focused responsibility
- **Comparative Analysis**: Cross-dimensional analysis (regions, products)
- **Export Flexibility**: Multi-format report generation (JSON, TXT, HTML, PDF)
- **Error Handling**: Comprehensive error management with custom exceptions
- **Logging**: Structured logging for production monitoring and debugging
- **Testing**: 27 unit tests with comprehensive coverage
- **Type Safety**: Full type hints throughout codebase
- **Configuration Management**: Environment-driven, token-reuse patterns
- **LLM Integration**: Real GitHub Marketplace API with cost optimization
- **Code Quality**: Clean code, SOLID principles, DRY methodology
- **Token Efficiency**: New agents reuse existing tokens (no additional costs)

## Supported Export Formats

| Format | Size | Use Case |
|--------|------|----------|
| **JSON** | Compact | Data integration, APIs |
| **TXT** | Lightweight | Email, archives |
| **HTML** | Styled | Web viewing, sharing |
| **PDF** | Professional | Print, formal reports |

## Future Enhancements

- [ ] Forecasting Agent (time-series predictions)
- [ ] Anomaly Detection Agent (identify outliers)
- [ ] Caching for identical queries
- [ ] Cost tracking per agent execution
- [ ] Async execution for parallel agent workflows
- [ ] REST API endpoint wrapper
- [ ] Database persistence for report history
- [ ] User feedback loop for prompt optimization
- [ ] Support for additional data sources

## License

MIT
