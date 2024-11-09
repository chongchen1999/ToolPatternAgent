import json
from typing import Callable, List, Dict, Union, get_origin, get_args
import typing

def get_fn_signature(fn: Callable) -> dict:
    """
    Generates the signature for a given function.

    Args:
        fn (Callable): The function whose signature needs to be extracted.

    Returns:
        dict: A dictionary containing the function's name, description,
              and parameter types.
    """
    fn_signature: dict = {
        "name": fn.__name__,
        "description": fn.__doc__,
        "parameters": {"properties": {}},
    }
    
    # Handle complex types
    schema = {}
    for k, v in fn.__annotations__.items():
        if k != "return":
            if hasattr(v, "__origin__"):  # For complex types like List, Dict
                origin = get_origin(v)
                args = get_args(v)
                if origin == list:
                    schema[k] = {"type": "List", "items_type": args[0].__name__}
                elif origin == dict:
                    schema[k] = {"type": "Dict", "key_type": args[0].__name__, "value_type": args[1].__name__}
            else:  # For simple types
                schema[k] = {"type": v.__name__}
    
    fn_signature["parameters"]["properties"] = schema
    return fn_signature


def validate_arguments(tool_call: dict, tool_signature: dict) -> dict:
    """
    Validates and converts arguments in the input dictionary to match the expected types.

    Args:
        tool_call (dict): A dictionary containing the arguments passed to the tool.
        tool_signature (dict): The expected function signature and parameter types.

    Returns:
        dict: The tool call dictionary with the arguments converted to the correct types if necessary.
    """
    properties = tool_signature["parameters"]["properties"]

    # Extended type mapping
    type_mapping = {
        "int": int,
        "str": str,
        "bool": bool,
        "float": float,
        "List": list,
        "Dict": dict
    }

    for arg_name, arg_value in tool_call["arguments"].items():
        type_info = properties[arg_name]
        expected_type = type_info["type"]

        # Handle basic types
        if expected_type in ["int", "str", "bool", "float"]:
            if not isinstance(arg_value, type_mapping[expected_type]):
                tool_call["arguments"][arg_name] = type_mapping[expected_type](arg_value)
        
        # Handle List type
        elif expected_type == "List":
            if not isinstance(arg_value, list):
                if isinstance(arg_value, str):
                    # Try to parse string as JSON if it's a string representation of a list
                    try:
                        tool_call["arguments"][arg_name] = json.loads(arg_value)
                    except json.JSONDecodeError:
                        tool_call["arguments"][arg_name] = [arg_value]
                else:
                    tool_call["arguments"][arg_name] = [arg_value]
        
        # Handle Dict type
        elif expected_type == "Dict":
            if not isinstance(arg_value, dict):
                if isinstance(arg_value, str):
                    # Try to parse string as JSON if it's a string representation of a dict
                    try:
                        tool_call["arguments"][arg_name] = json.loads(arg_value)
                    except json.JSONDecodeError:
                        tool_call["arguments"][arg_name] = {}

    return tool_call

class Tool:
    """
    A class representing a tool that wraps a callable and its signature.

    Attributes:
        name (str): The name of the tool (function).
        fn (Callable): The function that the tool represents.
        fn_signature (str): JSON string representation of the function's signature.
        tool_definition (dict): The function signature, used for testing.
    """

    def __init__(self, name: str, fn: Callable, fn_signature: str):
        self.name = name
        self.fn = fn
        self.fn_signature = fn_signature
        self.tool_definition = json.loads(fn_signature)  # Store the parsed signature for testing

    def __str__(self):
        return self.fn_signature

    def run(self, **kwargs):
        """
        Executes the tool (function) with provided arguments.

        Args:
            **kwargs: Keyword arguments passed to the function.

        Returns:
            The result of the function call.
        """
        return self.fn(**kwargs)

def tool(fn: Callable):
    """
    A decorator that wraps a function into a Tool object and adds a tool_definition attribute.

    Args:
        fn (Callable): The function to be wrapped.

    Returns:
        Tool: A Tool object containing the function, its name, and its signature.
    """
    fn_signature = get_fn_signature(fn)
    
    # Create the Tool object and assign tool_definition
    tool_obj = Tool(
        name=fn_signature.get("name"), fn=fn, fn_signature=json.dumps(fn_signature)
    )
    
    return tool_obj
