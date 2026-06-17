import pandas as pd
from langchain.tools import tool

@tool
def load_and_analyze(query: str) -> str:
    """Use this tool for ANY question about the sales data. 
    Pass the user's question as the query parameter.
    This tool loads the data and returns everything needed to answer."""
    try:
        df = pd.read_csv("data/sample_sales.csv")
        
        # Pre-compute common analyses so LLM can answer without extra tool calls
        by_region = df.groupby("region")["sales"].sum().to_string() if "region" in df.columns else "no region column"
        by_month  = df.groupby("month")["sales"].sum().sort_values(ascending=False).to_string() if "month" in df.columns else "no month column"
        top3      = df.groupby("month")["sales"].sum().sort_values(ascending=False).head(3).to_string() if "month" in df.columns else ""
        
        return f"""
Query: {query}

--- Full Data ---
{df.to_string()}

--- Sales by Region ---
{by_region}

--- Sales by Month (sorted) ---
{by_month}

--- Top 3 Months ---
{top3}

--- Stats ---
{df.describe().to_string()}
        """.strip()
    except Exception as e:
        return f"Error: {str(e)}"