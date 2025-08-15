"""
Custom tools for Vietnamese stock market analysis
"""

import os
import warnings
from typing import Dict, Any
import pandas as pd
from vnstock import Vnstock

from crewai_tools import CodeInterpreterTool, BraveSearchTool

# Suppress warnings
warnings.filterwarnings("ignore")


class FinancialDataTool:
    """
    Tool for fetching and processing Vietnamese financial data using vnstock.
    """
    
    def __init__(self):
        """Initialize the financial data tool."""
        self.code_interpreter = CodeInterpreterTool()
    
    def _process_ratio_dataframe(self, ratios_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the financial ratios DataFrame to ensure consistent column naming.
        
        Args:
            ratios_df: Raw ratios DataFrame with multi-index columns
            
        Returns:
            pd.DataFrame: Processed DataFrame with flattened column names
        """
        if ratios_df.empty:
            return ratios_df
            
        try:
            # Create a copy to avoid modifying the original
            processed_df = ratios_df.copy()
            
            # Flatten multi-index columns by combining level 0 and level 1
            if isinstance(processed_df.columns, pd.MultiIndex):
                # Create new column names by combining the multi-index levels
                new_columns = []
                for col in processed_df.columns:
                    if col[0] == 'Meta':
                        # Keep meta columns as is
                        new_columns.append(col[1])
                    else:
                        # Use the English category and metric names directly
                        category = col[0].replace(' ', '_').replace('-', '_')
                        metric = col[1].replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'Pct').replace('.', '').replace('/', '_to_')
                        new_columns.append(f"{category}_{metric}")
                
                # Apply new column names
                processed_df.columns = new_columns
                
                print(f"✅ Processed financial ratios DataFrame with {len(new_columns)} columns")
            else:
                # Single-level columns - already in English, just clean them
                processed_df.columns = [col.replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'Pct').replace('.', '').replace('/', '_to_') for col in processed_df.columns]
                print(f"✅ Cleaned financial ratios DataFrame with {len(processed_df.columns)} columns")
                
            return processed_df
            
        except Exception as e:
            print(f"⚠️ Warning: Could not process ratios DataFrame: {str(e)}")
            return ratios_df
    
    def fetch_financial_data(self, stock_symbol: str) -> Dict[str, Any]:
        """
        Fetch comprehensive financial data for a given stock symbol.
        
        Args:
            stock_symbol: Vietnamese stock symbol (e.g., 'VIC', 'REE', 'VHM')
            
        Returns:
            Dict containing various financial dataframes
        """
        try:
            # Initialize vnstock
            stock = Vnstock().stock(symbol=stock_symbol, source="VCI")
            company = Vnstock().stock(symbol=stock_symbol, source="TCBS").company
            
            # Fetch raw financial data
            raw_ratios = stock.finance.ratio(period="year", lang="en", dropna=True)
            
            # Process the ratios DataFrame to handle multi-index columns
            processed_ratios = self._process_ratio_dataframe(raw_ratios)
            
            # Fetch other financial data
            financial_data = {
                'cash_flow': stock.finance.cash_flow(period="year"),
                'balance_sheet': stock.finance.balance_sheet(period="year", lang="en", dropna=True),
                'income_statement': stock.finance.income_statement(period="year", lang="en", dropna=True),
                'financial_ratios': processed_ratios,
                'dividend_schedule': company.dividends(),
                'stock_symbol': stock_symbol
            }
            
            print(f"✅ Successfully fetched financial data for {stock_symbol}")
            print(f"   - Processed ratios columns: {list(processed_ratios.columns) if not processed_ratios.empty else 'Empty'}")
            return financial_data
            
        except Exception as e:
            print(f"❌ Error fetching data for {stock_symbol}: {str(e)}")
            return {}


class NewsSearchTool:
    """
    Tool for searching financial news and market intelligence.
    """
    
    def __init__(self):
        """Initialize the news search tool."""
        self.brave_search = BraveSearchTool(n_results=3)
    
    def search_company_news(self, company_name: str, stock_symbol: str, search_type: str = "general") -> str:
        """
        Search for company-specific news and information.
        
        Args:
            company_name: Full company name
            stock_symbol: Stock ticker symbol
            search_type: Type of search ('general', 'financial', 'strategy', 'management')
            
        Returns:
            str: Search results
        """
        search_queries = {
            'general': f"{company_name} {stock_symbol} news Vietnam",
            'financial': f"{company_name} financial results earnings Vietnam",
            'strategy': f"{company_name} future plans strategy Vietnam",
            'management': f"{company_name} CEO management outlook Vietnam"
        }
        
        query = search_queries.get(search_type, search_queries['general'])
        
        try:
            results = self.brave_search._run(query)
            return results
        except Exception as e:
            print(f"⚠️ Warning: Search failed for {query}: {str(e)}")
            return f"Search failed for {query}"