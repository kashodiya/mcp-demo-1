# Internal FR - Source Code
import requests
from fastmcp import FastMCP, Client
from typing import Dict, Any, List, Union
import os
import inspect

mcp = FastMCP("BMO MCP Server")

BASE_URL = os.getenv('BASE_URL')

print(f"BASE_URL: {BASE_URL}")

def call_api(url_path, http_method, query_params, payload) -> Union[Dict[str, Any], None]:
    """
    Call an API with the given parameters and return the JSON response.
    
    :param url_path: The path to append to the base URL.
    :param http_method: The HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'DELETE').
    :param query_params: A dictionary of query parameters.
    :param payload: The payload to send in the request body (for POST, PUT, etc.).
    :return: The JSON response from the API.
    """
    # Construct the full URL
    full_url = f"{BASE_URL}{url_path}"

    print(f"*** Calling URL: {full_url}")
    print(f"*** query_params: {query_params}")

    headers = {
    }
    
    # Choose the appropriate request method
    if http_method == 'get':
        response = requests.get(full_url, params=query_params, headers=headers, verify=False)
    elif http_method == 'post':
        response = requests.post(full_url, params=query_params, json=payload, headers=headers, verify=False)
    elif http_method == 'put':
        response = requests.put(full_url, params=query_params, json=payload, headers=headers, verify=False)
    elif http_method == 'delete':
        response = requests.delete(full_url, params=query_params, headers=headers, verify=False)
    else:
        raise ValueError(f"Unsupported HTTP method: {http_method}")
    
    # Check for HTTP errors
    response.raise_for_status()
    
    # Return the JSON response
    return response.json()


def replace_placeholders_in_path(path, params, param_values):
    for param in params:
        placeholder = f"{{{param['name']}}}"
        if param['name'] in path:
            print(f"*** {param['name']}, {param_values}")
            path = path.replace(placeholder, param_values[param['var_name']])
            # path = path.replace(placeholder, param['value'])
    return path

