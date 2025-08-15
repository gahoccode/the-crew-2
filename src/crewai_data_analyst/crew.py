"""
CrewAI Financial Data Analyst Crew
This module orchestrates the financial analysis crew with configuration-based setup.
"""

import os
import warnings
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import yaml
import pandas as pd
from vnstock import Vnstock, Listing

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from .tools.custom_tool import FinancialDataTool, NewsSearchTool

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()


class FinancialAnalysisCrew:
    """
    CrewAI-based financial analysis crew with configuration-driven setup.
    """
    
    def __init__(self, openai_api_key: str = None):
        """
        Initialize the Financial Analysis Crew.
        
        Args:
            openai_api_key: OpenAI API key for the LLM
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Load configurations
        self.agents_config = self._load_config("config/agents.yaml")
        self.tasks_config = self._load_config("config/tasks.yaml")
        
        # Initialize LLM
        self.llm = LLM(
            model="gpt-4.1-mini",
            api_key=self.openai_api_key
        )
        
        # Initialize tools
        self.financial_tool = FinancialDataTool()
        self.news_tool = NewsSearchTool()
        
        # Create agents
        self.agents = self._create_agents()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        config_file = os.path.join(os.path.dirname(__file__), config_path)
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Create agents from configuration."""
        agents = {}
        
        for agent_name, config in self.agents_config.items():
            tools = []
            
            # Map tool names to actual tool instances
            tool_mapping = {
                'code_interpreter': self.financial_tool.code_interpreter,
                'brave_search': self.news_tool.brave_search
            }
            
            for tool_name in config.get('tools', []):
                if tool_name in tool_mapping:
                    tools.append(tool_mapping[tool_name])
            
            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                tools=tools,
                llm=self.llm,
                **config.get('settings', {})
            )
            
            agents[agent_name] = agent
        
        return agents
    
    def _create_task(self, task_name: str, agent_name: str, **context) -> Task:
        """Create a task from configuration with context."""
        task_config = self.tasks_config[task_name]
        
        # Create data context for financial analysis tasks
        data_context = ""
        if 'financial_data' in context:
            financial_data = context['financial_data']
            data_context = f"""
        FETCHED DATA FOR PANDAS OPERATIONS:
        
        # Income Statement DataFrame (use this exact data):
        income_statement_data = {financial_data['income_statement'].to_dict('records') if not financial_data['income_statement'].empty else []}
        income_statement_columns = {list(financial_data['income_statement'].columns) if not financial_data['income_statement'].empty else []}
        
        # Balance Sheet DataFrame (use this to query key financial metrics):
        balance_sheet_data = {financial_data['balance_sheet'].to_dict('records') if not financial_data['balance_sheet'].empty else []}
        balance_sheet_columns = {list(financial_data['balance_sheet'].columns) if not financial_data['balance_sheet'].empty else []}
        
        # Financial Ratios DataFrame (use this exact data):
        financial_ratios_data = {financial_data['financial_ratios'].to_dict('records') if not financial_data['financial_ratios'].empty else []}
        financial_ratios_columns = {list(financial_data['financial_ratios'].columns) if not financial_data['financial_ratios'].empty else []}
        
        # Cash Flow DataFrame (use this exact data):
        cash_flow_data = {financial_data['cash_flow'].to_dict('records') if not financial_data['cash_flow'].empty else []}
        cash_flow_columns = {list(financial_data['cash_flow'].columns) if not financial_data['cash_flow'].empty else []}
        
        # Dividend Schedule DataFrame (use this exact data):
        dividend_data = {financial_data['dividend_schedule'].to_dict('records') if not financial_data['dividend_schedule'].empty else []}
        dividend_columns = {list(financial_data['dividend_schedule'].columns) if not financial_data['dividend_schedule'].empty else []}
        """
            context['data_context'] = data_context
        
        # Format description with context
        description = task_config['description'].format(**context)
        
        return Task(
            description=description,
            expected_output=task_config['expected_output'],
            agent=self.agents[task_config['agent']]
        )
    
    def fetch_financial_data(self, stock_symbol: str) -> Dict[str, pd.DataFrame]:
        """
        Fetch comprehensive financial data for a given stock symbol.
        
        Args:
            stock_symbol: Vietnamese stock symbol (e.g., 'VIC', 'REE', 'VHM')
            
        Returns:
            Dict containing various financial dataframes
        """
        return self.financial_tool.fetch_financial_data(stock_symbol)
    
    def get_company_info(self, stock_symbol: str) -> tuple[str, str]:
        """
        Fetch company information from vnstock API.
        
        Args:
            stock_symbol: Stock symbol to get company info for
            
        Returns:
            tuple: (company_name, industry)
        """
        try:
            listing = Listing()
            stock_list = listing.symbols_by_industries()
            
            # Find the specific stock information
            stock_info = stock_list[stock_list['symbol'] == stock_symbol.upper()]
            
            if not stock_info.empty:
                company_name = str(stock_info.iloc[0]['organ_name'])
                industry = str(stock_info.iloc[0]['icb_name3'])
            else:
                company_name = stock_symbol
                industry = ""
                
            return company_name, industry
            
        except Exception as e:
            print(f"⚠️ Warning: Could not fetch company info for {stock_symbol}: {str(e)}")
            return stock_symbol, ""
    
    def run_analysis(self, stock_symbol: str, analysis_type: str = "comprehensive") -> str:
        """
        Run the financial analysis and news research for a given stock.
        
        Args:
            stock_symbol: Stock symbol to analyze
            analysis_type: Type of analysis ('comprehensive', 'profitability', 'liquidity')
            
        Returns:
            str: Analysis results
        """
        try:
            # Fetch company information and financial data
            company_name, industry = self.get_company_info(stock_symbol)
            financial_data = self.fetch_financial_data(stock_symbol)
            
            if not financial_data:
                raise ValueError(f"Could not fetch financial data for {stock_symbol}")
            
            print(f"📊 Company Info: {company_name} ({stock_symbol}) - Industry: {industry or 'N/A'}")
            
            # Create context for tasks
            context = {
                'stock_symbol': stock_symbol,
                'company_name': company_name,
                'industry': industry,
                'financial_data': financial_data
            }
            
            # Create tasks based on analysis type
            if analysis_type == "comprehensive":
                analysis_task = self._create_task('financial_analysis', 'financial_data_analyst', **context)
            elif analysis_type == "profitability":
                analysis_task = self._create_task('profitability_analysis', 'financial_data_analyst', **context)
            elif analysis_type == "liquidity":
                analysis_task = self._create_task('liquidity_analysis', 'financial_data_analyst', **context)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            news_task = self._create_task('news_research', 'news_research_analyst', **context)
            
            # Create and run the crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=[analysis_task, news_task],
                process=Process.sequential,
                verbose=True,
                memory=True
            )
            
            print(f"🚀 Starting financial analysis and news research for {stock_symbol}...")
            result = crew.kickoff()
            
            print(f"✅ Analysis and news research completed for {stock_symbol}")
            
            # Export findings to files
            self._export_reports(stock_symbol, analysis_type, result)
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _export_reports(self, stock_symbol: str, analysis_type: str, result) -> None:
        """Export analysis results to report files."""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Export financial analysis report
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                report_content = f"""# Financial Analysis Report

**Stock Symbol:** {stock_symbol}  
**Analysis Type:** {analysis_type.title()}  
**Generated:** {timestamp}  
**Generated by:** CrewAI Financial Analysis Crew

---

{result.tasks_output[0]}

---

*This report was automatically generated by the CrewAI Financial Analysis Crew.*
"""
                with open("report.md", 'w', encoding='utf-8') as f:
                    f.write(report_content)
                print("✅ Report exported to report.md")
            
            # Export news research report
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 1:
                with open("news.md", "w", encoding="utf-8") as f:
                    f.write(f"# {stock_symbol} - Recent News & Market Intelligence\n\n")
                    f.write(f"**Generated on:** {timestamp}\n\n")
                    f.write("---\n\n")
                    f.write(str(result.tasks_output[1]))
                    f.write("\n\n---\n\n")
                    f.write("*This report was generated using CrewAI with news research capabilities.*\n")
                print("✅ News report exported to news.md")
                
        except Exception as e:
            print(f"⚠️ Warning: Could not export reports: {str(e)}")


# Legacy support - maintain the old FinancialDataAnalyst class name for backward compatibility
FinancialDataAnalyst = FinancialAnalysisCrew