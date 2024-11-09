# external_service.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from typing import Dict, List, Optional
import requests
from datetime import datetime, timedelta
from tool_agent import ToolAgent
from tool import tool

@tool
def get_trending_repos(language: str = "", since: str = "daily", limit: int = 10) -> List[Dict]:
    """
    Get trending GitHub repositories.

    Args:
        language (str): Programming language filter (e.g., 'python', 'javascript')
        since (str): Time range ('daily', 'weekly', 'monthly')
        limit (int): Maximum number of repositories to return

    Returns:
        List[Dict]: List of trending repositories with their details
    """
    # GitHub API token should be set in environment variable
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Calculate date based on 'since' parameter
    date_mapping = {
        'daily': 1,
        'weekly': 7,
        'monthly': 30
    }
    date_limit = datetime.now() - timedelta(days=date_mapping.get(since, 1))
    date_str = date_limit.strftime('%Y-%m-%d')
    
    # Construct query for GitHub Search API
    query = f"created:>{date_str}"
    if language:
        query += f" language:{language}"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}' if GITHUB_TOKEN else None
    }
    
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repos = response.json()['items']
        
        return [{
            'name': repo['full_name'],
            'description': repo['description'],
            'url': repo['html_url'],
            'language': repo['language'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at']
        } for repo in repos]
        
    except Exception as e:
        return [{"error": f"Failed to fetch trending repositories: {str(e)}"}]

@tool
def get_repo_contributors(repo_name: str, limit: int = 5) -> List[Dict]:
    """
    Get top contributors for a specific repository.

    Args:
        repo_name (str): Repository name in format 'owner/repo'
        limit (int): Maximum number of contributors to return

    Returns:
        List[Dict]: List of top contributors with their details
    """
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}' if GITHUB_TOKEN else None
    }
    
    try:
        url = f"https://api.github.com/repos/{repo_name}/contributors"
        params = {'per_page': limit}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        contributors = response.json()
        
        return [{
            'username': contributor['login'],
            'profile_url': contributor['html_url'],
            'contributions': contributor['contributions'],
            'avatar_url': contributor['avatar_url']
        } for contributor in contributors]
        
    except Exception as e:
        return [{"error": f"Failed to fetch contributors: {str(e)}"}]

@tool
def search_repo_issues(repo_name: str, state: str = "open", label: str = "", limit: int = 5) -> List[Dict]:
    """
    Search issues in a specific repository.

    Args:
        repo_name (str): Repository name in format 'owner/repo'
        state (str): Issue state ('open', 'closed', 'all')
        label (str): Filter by issue label
        limit (int): Maximum number of issues to return

    Returns:
        List[Dict]: List of matching issues with their details
    """
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}' if GITHUB_TOKEN else None
    }
    
    try:
        url = f"https://api.github.com/repos/{repo_name}/issues"
        params = {
            'state': state,
            'labels': label,
            'per_page': limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        return [{
            'title': issue['title'],
            'number': issue['number'],
            'state': issue['state'],
            'url': issue['html_url'],
            'created_at': issue['created_at'],
            'updated_at': issue['updated_at'],
            'comments': issue['comments'],
            'labels': [label['name'] for label in issue['labels']]
        } for issue in issues]
        
    except Exception as e:
        return [{"error": f"Failed to fetch issues: {str(e)}"}]

# Example usage:
if __name__ == "__main__":
    agent = ToolAgent([get_trending_repos, get_repo_contributors, search_repo_issues])

    # Example queries
    print("\nFetching trending Python repositories:")
    trending_response = agent.run("Find trending Python repositories from the last week")
    print(trending_response)

    # If we found repositories, get contributors for the first one
    if trending_response and isinstance(trending_response, list) and len(trending_response) > 0:
        first_repo = trending_response[0]['name']
        print(f"\nFetching top contributors for {first_repo}:")
        contributors_response = agent.run(f"Get top contributors for {first_repo}")
        print(contributors_response)

        print(f"\nFetching open issues for {first_repo}:")
        issues_response = agent.run(f"Find open issues in {first_repo} with label 'bug'")
        print(issues_response)