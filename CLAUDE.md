# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
CrewAI Financial Data Analyst - A multi-agent AI system for Vietnamese stock market analysis using CrewAI framework, vnstock data integration, and web-based market intelligence gathering.

## Development Commands

### Environment Setup
```bash
# Install dependencies using UV (recommended)
uv pip install -e .

# Or using pip
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env to add your API keys:
# OPENAI_API_KEY=your_openai_api_key_here
# BRAVE_API_KEY=your_brave_search_api_key_here
```

### Running the Application
```bash
# Run via command line (new structured approach)
python -m crewai_data_analyst.main

# Run via UV script entry point
the-crew-2

# Or alternative entry point
run_crew

# Legacy Streamlit interface (if app.py still exists)
streamlit run src/crewai_data_analyst/app.py
```

### Development Utilities
```bash
# Clean generated reports
./delete_reports.sh

# Generate reports manually
python src/crewai_data_analyst/app.py
```

## Code Architecture

### New Structured Architecture
The application now follows a configuration-driven approach with clear separation of concerns:

#### Directory Structure
```
src/crewai_data_analyst/
├── __init__.py              # Package initialization
├── main.py                  # Entry points and CLI interface  
├── crew.py                  # Main crew orchestration logic
├── app.py                   # Legacy Streamlit interface (if kept)
├── config/                  # Configuration files
│   ├── agents.yaml         # Agent definitions and settings
│   └── tasks.yaml          # Task templates and descriptions
└── tools/                   # Custom tools and utilities
    ├── __init__.py
    └── custom_tool.py      # Financial data and news search tools
```

#### Core Components

1. **FinancialAnalysisCrew** (`crew.py`)
   - Configuration-driven crew management
   - YAML-based agent and task definition loading
   - Orchestrates financial analysis and news research
   - Handles data fetching and report generation

2. **Agent Configuration** (`config/agents.yaml`)
   - **financial_data_analyst**: Senior Financial Data Analyst with CodeInterpreterTool
   - **news_research_analyst**: Financial News Research Analyst with BraveSearchTool
   - Centralized agent settings: LLM config, tools, behavior parameters

3. **Task Templates** (`config/tasks.yaml`)
   - **financial_analysis**: Comprehensive financial analysis template
   - **profitability_analysis**: Focused profitability analysis
   - **liquidity_analysis**: Liquidity and working capital analysis  
   - **news_research**: Market intelligence and company news research

4. **Custom Tools** (`tools/custom_tool.py`)
   - **FinancialDataTool**: vnstock integration and data processing
   - **NewsSearchTool**: Brave Search integration for market intelligence
   - Encapsulates data fetching and processing logic

#### Key Data Processing Components

**vnstock Integration** (`tools/custom_tool.py:FinancialDataTool`)
- Fetches Vietnamese stock market data from multiple sources (VCI, TCBS)
- Handles complex multi-index DataFrames with Vietnamese column names
- Processes financial statements: income, balance sheet, cash flow, ratios, dividends

**Data Processing Pipeline** (`tools/custom_tool.py:_process_ratio_dataframe`)
- **Challenge Solved**: vnstock returns Vietnamese multi-index columns
- **Solution**: Flattens to English format with standardized naming
- **Result**: Columns like `Profitability_ROE_Pct`, `Liquidity_Current_Ratio`

**Configuration-Driven Tasks** (`crew.py:_create_task`)
- Dynamic task creation from YAML templates
- Context injection for stock symbol, company info, financial data
- Flexible analysis type selection (comprehensive, profitability, liquidity)

### Legacy Compatibility
The refactored code maintains backward compatibility:
- `FinancialDataAnalyst` class alias in `crew.py` for legacy imports
- Existing entry points continue to work
- Same API for `run_analysis()` method

### Critical Configuration Details

#### LLM Configuration (`crew.py`)
```python
self.llm = LLM(
    model="gpt-4.1-mini",  # Primary model for financial analysis
    api_key=self.openai_api_key
)
```

#### Agent Configuration (`config/agents.yaml`)
```yaml
financial_data_analyst:
  role: "Senior Financial Data Analyst"
  tools: [code_interpreter]
  settings:
    allow_code_execution: true
    memory: true
    reasoning: true
```

#### Agent Optimization Settings
- `max_iter=2` - Limits agent iterations for efficiency
- `reasoning=True` - Enables planning, reflection, refinement
- `max_reasoning_attempts=2` - Balances quality vs performance
- `memory=True` - Maintains context across tasks

#### Process Coordination (`app.py:418-426`)
```python
# Current: Sequential processing
process=Process.sequential

# Alternative: Parallel processing (requires uncommenting)
# process=Process.hierarchical
# manager_llm=self.llm
```

### Data Sources and APIs
- **vnstock**: Vietnamese stock market data (financial statements, ratios, market data)
- **Brave Search**: Company news and market intelligence
- **OpenAI**: GPT-4.1-mini for financial analysis and reasoning

### Output Management
- **report.md**: Technical financial analysis with quantitative insights
- **news.md**: Market intelligence and company news research  
- **Streamlit Interface**: Interactive web UI at `http://localhost:8501`

### Project Structure Context
```
src/crewai_data_analyst/
├── app.py          # Main FinancialDataAnalyst class and agent definitions
├── main.py         # CLI entry points (kickoff, run_crew)
└── __init__.py     # Package initialization
```

## Important Implementation Notes

### Multi-Index DataFrame Handling
Vietnamese financial data requires special processing due to complex column structures. The `_process_ratio_dataframe()` method is critical for agent data access.

### Agent Coordination Strategy
The system uses sequential processing by default to ensure data consistency. The parallel option (hierarchical) is available but requires careful coordination to prevent race conditions in company data fetching.

### API Requirements
Both OPENAI_API_KEY and BRAVE_API_KEY are required for full functionality. The system will fail gracefully with clear error messages if keys are missing.

### Model Recommendations
- **Primary**: GPT-4.1-mini for financial analysis quality
- **Alternative**: GPT-4o-mini for cost optimization (may occasionally fail on complex data structures)
- **Research Agent**: Can use lower-tier models for general news gathering

### Testing Stock Symbols
Default analysis target is "REE" (Refrigeration Electrical Engineering Corporation). Common Vietnamese symbols: VIC, VNM, REE, VHM, HPG.