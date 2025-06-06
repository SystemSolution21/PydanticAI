"""
Module for handling OpenAI API errors with clean, readable error messages.
"""

from getpass import getpass
from typing import Optional, Tuple

from openai import (
    OpenAIError,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
)


def handle_openai_error(error: Exception) -> Tuple[str, Optional[str]]:
    """
    Handle OpenAI API errors and return clean, readable error messages.
    Also handles prompting for a new API key in case of AuthenticationError.

    Args:
        error: The exception to handle

    Returns:
        A tuple containing:
            - str: The formatted, readable error message.
            - Optional[str]: A new API key if an authentication error prompted for one, otherwise None.
    """
    message_parts = []
    new_api_key_to_return: Optional[str] = None

    if isinstance(error, AuthenticationError):
        message_parts.append(f"Authentication Error: {error.message}")
        message_parts.append("Please check your API key and make sure it's valid.")
        # Prompt for a new API key
        new_api_key_to_return = getpass(prompt="Enter a new OpenAI API Key: ")

    elif isinstance(error, APIConnectionError):
        message_parts.append(f"Connection Error: {error.message}")
        message_parts.append(
            "Check your network settings, proxy configuration, or firewall rules."
        )

    elif isinstance(error, RateLimitError):
        message_parts.append(f"Rate Limit Error: {error.message}")
        message_parts.append(
            "You've hit the rate limit. Please wait before trying again."
        )

    elif isinstance(error, APIStatusError):
        # For any status error, extract useful information
        message_parts.append(f"API Status Error ({error.status_code}): {error.message}")
        if error.request_id:
            message_parts.append(f"Request ID: {error.request_id}")
        if hasattr(error, "code") and error.code:
            message_parts.append(f"Error code: {error.code}")

    elif isinstance(error, OpenAIError):
        # For other OpenAI errors, use the message attribute when available
        if hasattr(error, "message"):
            message_parts.append(f"OpenAI Error: {error.message}")  # type: ignore
        else:
            error_message = extract_error_message(error_str=str(object=error))
            message_parts.append(f"OpenAI Error: {error_message}")

    else:
        error_message: str = extract_error_message(error_str=str(object=error))
        # Check if this is an API key error that wasn't caught by the AuthenticationError check
        if "Incorrect API key provided" in error_message or "API key" in error_message:
            message_parts.append(f"Authentication Error: {error_message}")
            message_parts.append("Please check your API key and make sure it's valid.")
            # Prompt for a new API key
            new_api_key_to_return = getpass(prompt="Enter a new OpenAI API Key: ")
        else:
            message_parts.append(f"Unexpected error occurred: {error_message}")

    return "\n".join(message_parts), new_api_key_to_return


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
