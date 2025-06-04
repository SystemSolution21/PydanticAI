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
    except Exception as e:
        # Handle all errors
        new_api_key: str | None = handle_openai_error(e)
        if new_api_key:
            os.environ["OPENAI_API_KEY"] = new_api_key


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
