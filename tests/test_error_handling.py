import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tool_agent import ToolAgent
from tool import tool

def run_test():
    # Test Error Handling
    @tool
    def add(x: int, y: int) -> int:
        """Add two numbers"""
        return x + y

    agent = ToolAgent([add])
    response = agent.run("Add 3.14 and 0.99")
    print(response)

    assert "error" in str(response).lower(), "Should handle invalid inputs gracefully."

    print("Test passed!")

# Run the tests
if __name__ == "__main__":
    run_test()