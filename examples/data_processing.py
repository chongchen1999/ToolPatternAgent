# data_processing.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from typing import Dict, List, Union
import pandas as pd
import numpy as np
from tool_agent import ToolAgent
from tool import tool
import json

@tool
def analyze_time_series(data: List[Dict[str, Union[str, float]]], 
                       date_column: str,
                       value_column: str) -> Dict:
    """
    Analyze time series data and provide statistical insights.

    Args:
        data (List[Dict]): List of dictionaries containing time series data
        date_column (str): Name of the column containing dates
        value_column (str): Name of the column containing values to analyze

    Returns:
        Dict: Statistical analysis results
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)

        # Calculate basic statistics
        stats = {
            'mean': float(df[value_column].mean()),
            'median': float(df[value_column].median()),
            'std_dev': float(df[value_column].std()),
            'min': float(df[value_column].min()),
            'max': float(df[value_column].max()),
            'trend': 'increasing' if df[value_column].iloc[-1] > df[value_column].iloc[0] else 'decreasing'
        }

        # Add rolling average
        df['rolling_avg'] = df[value_column].rolling(window=3).mean()
        stats['rolling_averages'] = df['rolling_avg'].dropna().tolist()

        return stats
    except Exception as e:
        return {"error": f"Failed to analyze data: {str(e)}"}

@tool
def clean_dataset(data: List[Dict], 
                  columns: List[str], 
                  handle_nulls: str = 'drop') -> List[Dict]:
    """
    Clean and preprocess a dataset.

    Args:
        data (List[Dict]): Input dataset
        columns (List[str]): Columns to keep
        handle_nulls (str): Strategy for handling null values ('drop' or 'fill')

    Returns:
        List[Dict]: Cleaned dataset
    """
    try:
        df = pd.DataFrame(data)
        
        # Select specified columns
        df = df[columns]
        
        # Handle null values
        if handle_nulls == 'drop':
            df = df.dropna()
        else:
            df = df.fillna(df.mean(numeric_only=True))
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Convert back to list of dictionaries
        return df.to_dict('records')
    except Exception as e:
        return [{"error": f"Failed to clean dataset: {str(e)}"}]

# Example usage:
agent = ToolAgent([analyze_time_series, clean_dataset])

# Example data
sample_data = [
    {"date": "2024-01-01", "value": 10.0, "category": "A"},
    {"date": "2024-01-02", "value": 15.0, "category": "B"},
    {"date": "2024-01-03", "value": 12.0, "category": "A"}
]

# Example queries
cleaning_response = agent.run("Clean the dataset and keep date and value columns")
print(cleaning_response)

raw_string = cleaning_response
formatted_string = raw_string.replace('\\n', '\n').replace('\\"', '"')

# Writing formatted content to a file
file_path = "../data/formatted_articles.txt"
with open(file_path, 'w') as file:
    file.write(formatted_string)

print(f"Formatted articles have been written to {file_path}")