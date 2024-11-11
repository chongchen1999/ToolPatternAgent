import os
import sys
import json
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from typing import Dict, List
import requests
from tool_agent import ToolAgent
from tool import tool

@tool
def search_hackernews(query: str, limit: int = 5) -> List[Dict]:
    """
    Search HackerNews articles by keyword and save results to file.
    
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
        
        articles = [
            {
                'title': item['title'],
                'url': item['url'],
                'score': item['points']
            }
            for item in results if item.get('url')
        ]
        
        # Create data directory if it doesn't exist
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(data_dir, f'api_interaction_result.json')
        
        # Save results to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'query': query,
                'timestamp': timestamp,
                'results': articles
            }, f, indent=2)
            
        print(f"Results saved to: {filename}")
        return articles
        
    except Exception as e:
        error_msg = f"Failed to fetch articles: {str(e)}"
        print(error_msg)
        return [{"error": error_msg}]

# Example usage:
if __name__ == "__main__":
    agent = ToolAgent([search_hackernews])
    response = agent.run("Find recent articles about Python")
    print("Search Results:")
    print(json.dumps(response, indent=2))