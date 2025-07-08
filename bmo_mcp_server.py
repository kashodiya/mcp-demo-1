# Internal FR - Source Code
from typing import Dict, Any, List, Union
import os
import inspect
# from utils_mcp_server import call_api, replace_placeholders_in_path
from fastmcp import FastMCP, Client
import requests

mcp = FastMCP("BMO MCP Server sam-svc")

@mcp.tool()
def get_applications() -> Union[Dict[str, Any], None]: 
    """
    Call this method to get list of applications.
    
    Returns:
        The result will be in JSON format.
    """

    # Generate a key-val of param names and values of this tool function
    # Get the current frame
    frame = inspect.currentframe()
    # Get the arguments passed to the function
    args, _, _, values = inspect.getargvalues(frame)
    # Create a list of key-value pairs
    # param_values = [(arg, values[arg]) for arg in args if arg != 'self']
    param_values = {arg: values[arg] for arg in args if arg != 'self'}    
    # Always clean up the frame to avoid reference cycles
    del frame    

    path = "/applications"
    http_method = "get"
    payload = None
    query_params = None
    real_path = None
    parameters = None

    print(f"param_values: {param_values}")

    # if len(param_values) > 0:
    #     real_path = replace_placeholders_in_path(path, parameters, param_values)
    #     query_params = {param["name"]: param_values[param["var_name"]] for param in parameters if param["in"] == "query"}
    # else:
    #     real_path = path
    #     query_params = []

    # try:
    #     result = call_api(real_path, http_method, query_params, payload)
    #     print(result)
    #     return result
    # except requests.RequestException as e:
    #     print(f"An error occurred: {e}")
    #     return {"error": e}
    



if __name__ == "__main__":
    # mcp.run(transport="stdio")
    mcp.run(transport="sse", port=9008)
    
