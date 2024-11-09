import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from typing import Dict, List
import requests
from tool_agent import ToolAgent
from tool import tool

@tool
def search_hackernews(query: str, limit: int = 5) -> List[Dict]:
    """
    Search HackerNews articles by keyword.

    Args:
        query (str): Search term
        limit (int): Maximum number of results to return

    Returns:
        List[Dict]: List of matching articles with title, url, and score
    """
    # HN Search API endpoint
    url = f"http://hn.algolia.com/api/v1/search?query={query}&numericFilters=points>10"

    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()['hits'][:limit]

        return [
            {
                'title': item['title'],
                'url': item['url'],
                'score': item['points']
            }
            for item in results if item.get('url')
        ]
    except Exception as e:
        return [{"error": f"Failed to fetch articles: {str(e)}"}]
    

# Example usage:
agent = ToolAgent([search_hackernews])

# Example query
response = agent.run("Find recent articles about Python")
print(response)

# Expected output format:
[
    {
        'title': 'Python 3.12 Released',
        'url': 'https://www.python.org/downloads/release/python-3120/',
        'score': 1234
    },
    ...
]