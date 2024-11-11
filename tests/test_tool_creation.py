# test_tool_creation.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tool_agent import ToolAgent
from tool import tool

def run_test():
    # Test Tool Creation
    @tool
    def add(x: int, y: int) -> int:
        """Add two numbers"""
        return x + y

    # Verify tool decorator adds 'tool_definition' attribute
    assert hasattr(add, 'tool_definition'), "Tool decorator should add 'tool_definition' attribute to the function."

    print("Test passed!")

# Run the tests
if __name__ == "__main__":
    run_test()
