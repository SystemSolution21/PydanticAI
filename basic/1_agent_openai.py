import os

from dotenv import load_dotenv
from getpass import getpass

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.openai import OpenAIModel

import openai
from openai import OpenAIError, APIConnectionError, AuthenticationError, RateLimitError

# Load environment variables from .env file
load_dotenv()

# Confirm OpenAI API key
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass(prompt="Enter OpenAI API Key: ")

# Create model
model = OpenAIModel(model_name="gpt-4.1-nano-2025-04-14", provider="openai")

# Create agent
agent = Agent(model=model)


# Define agent with error handling
def agent_openai(user_prompt: str) -> None:
    try:
        result: AgentRunResult[str] = agent.run_sync(user_prompt=user_prompt)
        print(result.output)

    except AuthenticationError as e:
        print(f"Authentication Error: {e}")
        print("Please check your API key and make sure it's valid.")
        # Optionally prompt for a new API key
        os.environ["OPENAI_API_KEY"] = getpass(prompt="Enter a new OpenAI API Key: ")

    except APIConnectionError as e:
        print(f"Connection Error: {e}")
        print("Check your network settings, proxy configuration, or firewall rules.")

    except RateLimitError as e:
        print(f"Rate Limit Error: {e}")
        print("You've hit the rate limit. Please wait before trying again.")

    except OpenAIError as e:
        print(f"OpenAI API Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


# Main entrypoint
if __name__ == "__main__":
    while True:
        try:
            user_prompt: str = input(
                "Ask a question to OpenAI Agent (type 'q' to 'quit'): "
            )
            if user_prompt.lower() == "q":
                print("Goodbye!")
                break

            agent_openai(user_prompt=user_prompt)
        except KeyboardInterrupt:
            print("Goodbye!")
            break
