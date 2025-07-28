# CrewAI Data Analyst

An intelligent financial analysis system powered by CrewAI and vnstock, designed to provide comprehensive stock analysis with interactive visualizations.

## Features

- **CrewAI Integration**: Intelligent agent-based analysis
- **vnstock Support**: Vietnamese stock market data
- **Interactive Visualizations**: Rich charts and graphs
- **Streamlit Interface**: User-friendly web interface
- **Financial Health Analysis**: Key ratios and metrics
- **Real-time Data**: Latest financial statements and market data

## Installation

### Using UV (Recommended)
```bash
# Install dependencies
uv pip install -r requirements.txt

# Or using pyproject.toml
uv pip install -e .
```

### Using pip
```bash
pip install -r requirements.txt
```

## Usage

1. **Set up environment variables** (required for full functionality):
   ```bash
   # Create .env file for API keys
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "BRAVE_API_KEY=your_brave_search_api_key_here" >> .env
   ```

2. **Run the application**:
   ```bash
   streamlit run app.py
   ```

3. **Access the web interface**:
   - Open your browser to `http://localhost:8501`
   - Enter a Vietnamese stock symbol (e.g., VIC, VNM, REE)
   - Select analysis type
   - Click "Run Analysis"

## Architecture

### Components

1. **CrewAI Agents**:
   - **Senior Financial Data Analyst**: Comprehensive financial analysis with code interpreter capabilities
   - **Financial News Research Analyst**: Searches and analyzes recent company news and market intelligence

2. **Built-in Tools**:
   - **CodeInterpreterTool**: Enables Python code execution for data analysis and visualization
   - **BraveSearchTool**: Searches for recent company news and market information

3. **Data Processing**:
   - **vnstock Integration**: Fetches Vietnamese stock market data
   - **Pandas Processing**: Handles financial data transformation and analysis
   - **Report Generation**: Creates markdown reports for analysis results

4. **LLM Configuration**:
   - **Model**: GPT-4.1 (configured in app.py)
   - **Features**: Code execution, reasoning, memory capabilities
   - **Settings**: Optimized for financial analysis tasks

### Data Sources

- **Financial Statements**: Income statement, balance sheet, cash flow
- **Key Ratios**: Liquidity, profitability, leverage metrics
- **Dividend History**: Cash dividends and payment dates
- **Market Data**: Historical prices and trading volumes

## Example Analysis

The system provides:
- **Financial Health Score**: Based on key ratios
- **Revenue Trends**: Historical revenue patterns
- **Profitability Analysis**: ROA, ROE, net margins
- **Liquidity Assessment**: Current ratio, quick ratio
- **Leverage Analysis**: Debt-to-equity, interest coverage
- **Dividend Analysis**: Historical dividend payments

## Troubleshooting

### Common Issues

1. **vnstock data not loading**:
   - Check internet connection
   - Verify stock symbol exists
   - Try different data sources (VCI, TCBS)

2. **Visualization errors**:
   - Check data availability for selected symbol
   - Ensure required columns exist in datasets

## AI Model Recommendations

### Best Practices for Model Selection

This CrewAI financial analysis system requires high-performance AI models due to the complexity of financial data structures and reasoning tasks.

#### **Recommended Models**

**For Global Project (Primary):**
- **GPT-4.1** (Recommended)
  - Excellent performance on complex financial analysis
  - Reliable handling of data structures and calculations
  - Superior reasoning capabilities for financial metrics

**For Research Agent (Secondary):**
- **GPT-4o-mini** (Acceptable for research tasks)
  - Suitable for general research and data gathering
  - Cost-effective for non-critical analysis
  - May occasionally fail on complex data structures

#### **Critical Requirements**

**Financial Analyst Agent:**
- **Minimum:** GPT-4.1 or higher
- **Reasoning:** Complex financial calculations require advanced reasoning
- **Data Structures:** Must handle multi-dimensional financial datasets
- **Accuracy:** High precision required for investment decisions

#### **Model Performance Notes**

⚠️ **Important:** GPT-4o-mini will sometimes fail on the code interpreter tool when handling complex financial data structures and advanced reasoning tasks. This is particularly evident in:
- Multi-period financial ratio calculations
- Complex portfolio optimization algorithms
- Advanced risk assessment models
- Cross-sectional financial analysis

#### **Environment Setup**

```bash
# Set your preferred model in .env
OPENAI_MODEL_NAME=gpt-4.1
# or
OPENAI_MODEL_NAME=gpt-4o-mini
```

## Development

### Project Structure
```
crewai-data-analyst/
├── app.py                 # Main Streamlit application
├── pyproject.toml         # UV project configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .env                  # Environment variables (optional)
```

## License

This project is open source and available under the MIT License.
