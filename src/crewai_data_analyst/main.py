#!/usr/bin/env python3
"""
Main entry point for the CrewAI Financial Data Analyst application.
This file provides the standard CrewAI entry points for running the crew.
"""

import os
import sys
from .crew import FinancialAnalysisCrew

def kickoff():
    """
    Main entry point for running the CrewAI Financial Data Analyst.
    This function is called by the `crewai run` command.
    """
    try:
        print("🚀 Starting CrewAI Financial Analysis Crew...")
        print("=" * 60)
        
        # Check for OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY environment variable not set.")
            print("Please set your OpenAI API key:")
            print("export OPENAI_API_KEY='your-api-key-here'")
            return
        
        # Initialize the crew
        crew = FinancialAnalysisCrew()
        
        # Default stock to analyze
        stock_symbol = "REE"
        
        print(f"📊 Analyzing {stock_symbol} stock with CrewAI crew...")
        print("=" * 60)
        
        # Run comprehensive analysis
        result = crew.run_analysis(
            stock_symbol=stock_symbol,
            analysis_type="comprehensive"
        )
        
        print("\n" + "=" * 80)
        print("🎯 FINANCIAL ANALYSIS RESULTS")
        print("=" * 80)
        print(result)
        print("=" * 80)
        print("✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running CrewAI Financial Analysis Crew: {str(e)}")
        sys.exit(1)

def run_crew():
    """
    Alternative entry point for running the crew.
    This provides compatibility with different CrewAI versions.
    """
    kickoff()

def main():
    """
    Direct execution entry point.
    """
    kickoff()

if __name__ == "__main__":
    main()
