import os
import time
from dotenv import load_dotenv
from getpass import getpass

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.openai import OpenAIModel

# Import error handling module
from openai_error import handle_openai_error

# Load environment variables from .env file
load_dotenv()


# Define agent with error handling
def agent_openai(user_prompt: str) -> None:
    """
    Create and run an OpenAI agent with error handling.

    Args:
        user_prompt: The user's input prompt to send to the agent
    """
    # Create model
    model = OpenAIModel(model_name="gpt-4.1-nano-2025-04-14", provider="openai")

    # Create agent
    agent = Agent(model=model)

    # Confirm OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass(prompt="Enter OpenAI API Key: ")
        print("OpenAI API key is updated.")

    # Run agent
    try:
        result: AgentRunResult[str] = agent.run_sync(user_prompt=user_prompt)
        print(f"\nOpenAI Agent: {result.output}")

    except Exception as e:

        # Handle all errors
        error_message = handle_openai_error(error=e)
        print(error_message)

        # Authentication error
        if "Authentication Error" in error_message:
            # Clear the old API key
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]

            # Set the new API key
            os.environ["OPENAI_API_KEY"] = getpass(
                prompt="Enter a new OpenAI API Key: "
            )
            print("A new OpenAI API key is updated.")


# Main entrypoint
if __name__ == "__main__":
    while True:
        try:
            user_prompt: str = input(
                "\nAsk any question to the OpenAI Agent. Type 'q' to quit: "
            )
            if user_prompt.lower() in "q":
                print("Goodbye!")
                break

            agent_openai(user_prompt=user_prompt)
        except KeyboardInterrupt:
            print("Goodbye!")
            break
