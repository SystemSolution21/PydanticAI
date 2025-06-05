"""
Module for handling OpenAI API errors with clean, readable error messages.
"""

from getpass import getpass
from typing import Optional

from openai import (
    OpenAIError,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
)


def handle_openai_error(error: Exception) -> Optional[str]:
    """
    Handle OpenAI API errors and return clean, readable error messages.

    Args:
        error: The exception to handle

    Returns:
        Optional new API key if authentication error prompts for a new key
    """
    if isinstance(error, AuthenticationError):
        print(f"Authentication Error: {error.message}")
        print("Please check your API key and make sure it's valid.")
        # Prompt for a new API key
        new_api_key = getpass(prompt="Enter a new OpenAI API Key: ")
        return new_api_key

    elif isinstance(error, APIConnectionError):
        print(f"Connection Error: {error.message}")
        print("Check your network settings, proxy configuration, or firewall rules.")

    elif isinstance(error, RateLimitError):
        print(f"Rate Limit Error: {error.message}")
        print("You've hit the rate limit. Please wait before trying again.")

    elif isinstance(error, APIStatusError):
        # For any status error, extract useful information
        print(f"API Status Error ({error.status_code}): {error.message}")
        if error.request_id:
            print(f"Request ID: {error.request_id}")
        if hasattr(error, "code") and error.code:
            print(f"Error code: {error.code}")

    elif isinstance(error, OpenAIError):
        # For other OpenAI errors, use the message attribute when available
        if hasattr(error, "message"):
            print(f"OpenAI Error: {error.message}")  # type: ignore

        else:
            error_message = extract_error_message(error_str=str(object=error))
            print(f"OpenAI Error: {error_message}")

    else:
        error_message: str = extract_error_message(error_str=str(object=error))
        # Check if this is an API key error that wasn't caught by the AuthenticationError check
        if "Incorrect API key provided" in error_message or "API key" in error_message:
            print(f"Authentication Error: {error_message}")
            print("Please check your API key and make sure it's valid.")
            # Prompt for a new API key
            new_api_key = getpass(prompt="Enter a new OpenAI API Key: ")
            return new_api_key
        else:
            print(f"Unexpected error: {error_message}")

    return None


def extract_error_message(error_str: str) -> str:
    """Extract a clean error message from error string."""
    # Extract message from JSON-like error format
    if "'message': '" in error_str:
        error_str = (
            error_str.split(sep="'message': '")[1].split(sep="', 'type':")[0].strip()
        )
    # Extract message from HTML error format
    if "<h1>" in error_str:
        error_str = error_str.split(sep="<h1>")[1].split(sep="</h1>")[0].strip()

    return error_str
