import os
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
        print("OpenAI API key is set.")

    try:
        result: AgentRunResult[str] = agent.run_sync(user_prompt=user_prompt)
        print(f"OpenAI Agent: {result.output}")

    except Exception as e:
        # Handle all errors
        new_api_key: str | None = handle_openai_error(e)

        # If authentication error occurred and we got a new key
        if new_api_key:
            # Clear the old key first
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]

            # Set the new key
            os.environ["OPENAI_API_KEY"] = new_api_key
            print("OpenAI API key is set.")

            # Try again with the new API key
            try:
                result: AgentRunResult[str] = agent.run_sync(user_prompt=user_prompt)
                print(f"OpenAI Agent: {result.output}")

            except Exception as e:
                # If it fails again, handle the error but don't retry
                handle_openai_error(error=e)


# Main entrypoint
if __name__ == "__main__":
    print("Welcome to the OpenAI Agent CLI. Type 'q' to quit.")
    while True:
        try:
            user_prompt: str = input("\nYour question: ")
            if user_prompt.lower() in ["q", "quit", "exit"]:
                print("Goodbye!")
                break

            agent_openai(user_prompt=user_prompt)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
