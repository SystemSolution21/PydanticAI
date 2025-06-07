"""
Module for handling OpenAI API errors with clean, readable error messages.
"""

from openai import (
    OpenAIError,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
)


def handle_openai_error(error: Exception) -> str:
    """
    Handle OpenAI API errors and return clean, readable error messages.
    Also handles prompting for a new API key in case of AuthenticationError.

    Args:
        error: The exception to handle

    Returns:
        - str: The formatted, readable error message.
    """
    error_message: str = ""

    # Authentication error
    if isinstance(error, AuthenticationError):
        error_message = f"Authentication Error: {error.message}"
        error_message += " Please check your API key and make sure it's valid."

    # API Connection error
    elif isinstance(error, APIConnectionError):
        error_message = f"Connection Error: {error.message}"
        error_message += " Please check your network settings, proxy configuration, or firewall rules."

    # Rate limit error
    elif isinstance(error, RateLimitError):
        error_message = f"Rate Limit Error: {error.message}"
        error_message += " You've hit the rate limit. Please wait before trying again."

    # API Status error
    elif isinstance(error, APIStatusError):
        error_message = f"API Status Error ({error.status_code}): {error.message}"
        if error.request_id:
            error_message += f" Request ID: {error.request_id}"
        if hasattr(error, "code") and error.code:
            error_message += f" Error code: {error.code}"

    # OpenAI error
    elif isinstance(error, OpenAIError):
        if hasattr(error, "message"):
            error_message = f"OpenAI Error: {error.message}"  # type: ignore
        else:
            ext_err_mes = extract_error_message(error_str=str(object=error))
            error_message = f"OpenAI Error: {ext_err_mes}"

    # Other errors
    else:
        ext_err_mes: str = extract_error_message(error_str=str(object=error))
        if "Incorrect API key provided" in ext_err_mes or "API key" in ext_err_mes:
            error_message = f"Authentication Error: {ext_err_mes}"
            error_message += "Please check your API key and make sure it's valid."

        else:
            error_message = f"Unexpected error occurred: {ext_err_mes}"

    return error_message


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
