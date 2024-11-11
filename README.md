# LLM Tool Pattern Implementation

## Overview
This repository presents an implementation of a tool pattern that enhances the capabilities of Large Language Models (LLMs) by enabling them to interact with external functions. The project focuses on providing LLMs the ability to call tools for tasks such as data retrieval, processing, and integration with external APIs, which helps extend the LLM's utility beyond its training data. The interaction is facilitated by a structured XML-based prompt format that ensures reliable tool usage and error handling.

## Key Components

### 1. Tool System Prompt
* **Purpose**: A structured instructional prompt that guides the LLM in making tool calls using an XML-based format
* **Details**: XML tags like `<tool_call></tool_call>` and `<tools></tools>` encapsulate tool calls and available definitions, helping in structured parsing and execution

### 2. Tool Definition Format
* **Format**: JSON-based schema that describes each tool's function, parameters, and expected data types
* **Details**: Supports basic types like `int`, `str`, and complex structures like `List` and `Dict`

### 3. Tool Decorator
* **Function**: A Python decorator that wraps functions as tools, extracting metadata for type validation and XML parsing
* **Usage**: Ensures functions are ready for registration in the ToolAgent

### 4. Tool Agent
* **Role**: Manages tool execution and interaction with the LLM
* **Features**: Handles tool registration, argument validation, execution, and error reporting

## Example Tools

### 1. API Interaction Tool: search_hackernews
* **Functionality**: Retrieves articles from HackerNews based on a search term
* **Parameters**:
  * `query` (str): Search keyword
  * `limit` (int): Maximum number of results
* **Return**: List of articles with title, URL, and score

### 2. Data Processing Tool: analyze_time_series, clean_dataset
* **Features**:
  * `analyze_time_series`: Provides statistical insights into time series data
  * `clean_dataset`: Preprocesses data by handling nulls and removing duplicates
* **Parameters**:
  * `data` (List[Dict]): Dataset input
  * `date_column`, `value_column`, `columns`, etc.
* **Return**: Analytical results or cleaned dataset

### 3. External Service Integration Tool: GitHub Functions
* **Tools**:
  * `get_trending_repos`: Fetches trending repositories
  * `get_repo_contributors`: Lists contributors
  * `search_repo_issues`: Finds issues based on filters
* **Parameters**: Various GitHub-related criteria (e.g., `language`, `repo_name`)
* **Return**: Repositories, contributors, or issues list

## Testing

### Approach
Tests were developed to verify functionality, input validation, and error handling:
* **Basic Functionality Tests**: Confirm correct execution of tool functions
* **Error Handling Tests**: Ensure the system responds to invalid inputs appropriately

### Test Cases
* **Tool Creation and Attribute Check**: Ensures the tool decorator adds metadata to functions
* **Basic Function Execution**: Verifies registered functions execute as expected
* **Error Handling**: Tests input validation by running tools with incorrect parameters

## Project Success and Future Work

### Achievements
* Implemented a robust system for tool-based LLM interactions
* Ensured reliable execution and error handling
* Extended LLM applicability through external integration

### Potential Improvements
* **Dynamic Tool Discovery**: Automate the tool registration process
* **Advanced Error Handling**: Differentiate error types for tailored feedback
* **Multi-step Tool Execution**: Implement workflow support for chaining tool calls
* **Context-aware Responses**: Maintain session state for interactive tools
* **More Tool Integrations**: Include tools for web scraping and visualization

## How to Use

### Installation
1. Clone this repository:
```bash
git clone https://github.com/username/llm-tool-pattern.git
cd llm-tool-pattern
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage
1. Register tools by decorating functions with `@tool`
2. Create an instance of `ToolAgent` and register tools
3. Pass user queries to the `ToolAgent` to trigger tool executions

### Example Code Snippet
```python
from tool_agent import ToolAgent, tool

@tool
def add(x: int, y: int) -> int:
    """Adds two numbers."""
    return x + y

agent = ToolAgent()
agent.register_tool(add)

# Execute a tool function
result = agent.handle_query("<tool_call>{\"function\": \"add\", \"arguments\": {\"x\": 5, \"y\": 3}}</tool_call>")
print(result)  # Output: <tool_response>{"result": 8}</tool_response>
```