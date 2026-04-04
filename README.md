# 🤖 AI Data Team - Multi-Agent AI System

An autonomous multi-agent system that analyzes sales data, generates insights, and produces structured business reports using LLM-based agents.

## Architecture

```
User Query
    ↓
Planner Agent (decides workflow)
    ↓
┌─────────────────────────────────────────┐
│  Data Analyst  │  Comparison  │ Export  │
│     Agent      │    Agent     │ Agent   │
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

✅ **Web Dashboard** - Interactive Streamlit interface for non-technical users  
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

### 2. **Configure Environment (Optional)**

**For Portfolio Reviewers:** The dashboard includes a **Demo Mode** that works without any configuration! Simply run the dashboard and it will automatically detect demo mode, showing pre-computed sample analyses and fully functional export buttons.

**For Live AI Analysis:** To enable custom questions and real-time AI analysis, add your GitHub Marketplace API tokens.

#### Option A: Quick Start with Demo Mode (No Setup Required) 🎬
```bash
# Just run the dashboard - Demo Mode activates automatically
python start_dashboard.py
```
The dashboard detects missing tokens and enters Demo Mode, which includes:
- ✅ Dashboard with sample data and charts
- ✅ Pre-loaded sample questions with analysis results
- ✅ Full export functionality (PDF, JSON, HTML, TXT)
- ✅ Comparison reports with sample data
- ✅ All UI/UX features working

Perfect for: **Portfolio reviews, demonstrations, testing the UI**

#### Option B: Live AI Analysis with Your Tokens

1. **Start with the template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your GitHub Marketplace API tokens to `.env`:**
   - Get free tokens from: https://github.com/settings/tokens
   - Edit `.env` and replace `ghp_your_token_here` with your actual tokens

   ```env
   PLANNER_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
   ANALYST_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
   INSIGHT_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
   REPORT_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
   ```

3. **Start the dashboard:**
   ```bash
   python start_dashboard.py
   ```
   
   When tokens are configured, the dashboard will show ✅ **Live mode** and allow custom AI queries.

Perfect for: **Production use, custom analysis, full system capability**

**⚠️ Security Note:** The `.env` file is git-ignored and never committed. Your tokens remain completely private.

### 3. **Run the System**

#### Option A: Web Dashboard (Recommended for Non-Technical Users) 🌐

```bash
# Windows
run_dashboard.bat

# Mac/Linux
python start_dashboard.py
```

Then open your browser to **http://localhost:8501**

The web dashboard provides:
- 📊 **Dashboard** - View sales metrics and data overview
- 🔍 **Ask AI** - Chat-like interface to ask questions about your data (works in both demo and live modes!)
- 📈 **Comparisons** - Compare regions and products side-by-side
- 📄 **Reports** - View and download previously generated reports

**Works in Two Modes:**
- 🎬 **Demo Mode** (No tokens needed) - Shows sample analyses and fully functional UI
- ✅ **Live Mode** (With tokens) - Custom AI-powered analysis of your questions

**Perfect for**: Non-technical users, stakeholders, executives, portfolio demonstrations

#### Option B: Command-Line Interface

```bash
python main.py
```

Interactive CLI where you can ask questions and get instant analysis. (Requires `.env` configuration)

#### Option C: Run Tests

```bash
pytest tests/ -v
```

Run the comprehensive test suite (27 tests)

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

## 🎬 Demo Mode

The dashboard includes a **Demo Mode** that works immediately without any configuration. This is perfect for portfolio reviews, demos, and testing the UI.

### What's Included in Demo Mode?

| Feature | Demo Mode | Live Mode |
|---------|-----------|-----------|
| Dashboard with charts | ✅ | ✅ |
| Ask AI with sample questions | ✅ (Pre-loaded) | ✅ (Custom) |
| Export to PDF/JSON/HTML | ✅ | ✅ |
| Regional comparisons | ✅ (Sample) | ✅ (Real data) |
| Product comparisons | ✅ (Sample) | ✅ (Real data) |
| Custom AI questions | ❌ | ✅ |
| Requires API tokens | ❌ | ✅ |

### How It Works

1. **Run the dashboard** (no `.env` needed)
   ```bash
   python start_dashboard.py
   ```

2. **Dashboard automatically detects demo mode** and shows:
   - Sidebar warning: "🎬 DEMO MODE ACTIVE"
   - Banner at top: "Using sample data and pre-computed results"
   - All UI functional with pre-computed sample analyses

3. **Portfolio reviewers can:**
   - Browse the Dashboard tab with real sales metrics
   - Select from sample questions in Ask AI mode
   - View analysis results instantly
   - Export results as PDF with custom filename
   - Test comparisons with sample regional/product data
   - Download reports

4. **No token errors, no API delays** - everything works smoothly

### Upgrading from Demo to Live Mode

When you want to enable live AI analysis:
```bash
cp .env.example .env
# Edit .env and add your GitHub Marketplace tokens
python start_dashboard.py
```

The dashboard automatically switches to Live Mode when valid tokens are found.

## Project Structure

```
ai-agents-journey-new/
├── main.py                          # Entry point & orchestration loop (CLI)
├── streamlit_app.py                 # Web dashboard (Streamlit)
├── start_dashboard.py               # Cross-platform dashboard launcher
├── run_dashboard.bat                # Windows dashboard launcher
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
├── .env.example                     # Environment template (copy to .env to configure)
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
