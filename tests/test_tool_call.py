import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tool_agent import ToolAgent
from tool import tool

def run_test():
    # Test Tool Call
    @tool
    def add(x: int, y: int) -> int:
        """Add two numbers"""
        return x + y

    agent = ToolAgent([add])
    response = agent.run("Add 5 and 3")
    print(response)
    assert "8" in response, "Basic addition should work"

    print("Test passed!")

# Run the tests
if __name__ == "__main__":
    run_test()
