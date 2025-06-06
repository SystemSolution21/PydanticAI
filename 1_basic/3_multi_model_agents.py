import os

from getpass import getpass

from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.messages import ModelRequest, ModelResponse
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


# Load environment variables from .env file
load_dotenv()

# Confirm OpenAI API key
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass(prompt="Enter OpenAI API Key: ")
    print("OpenAI API key is set.\n")

# Create OpenAI model
openai_model = OpenAIModel(model_name="gpt-4.1-nano-2025-04-14", provider="openai")

# Create OpenAI agent
openai_agent = Agent(model=openai_model)

# Create ollama model
ollama_model = OpenAIModel(
    model_name="gemma3:4b",
    provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
)

# Create ollama agent
ollama_agent = Agent(model=ollama_model)

# Main entrypoint
if __name__ == "__main__":
    print("Welcome to the Multi-Model Agent CLI. Type 'q' to quit.")
    while True:
        try:
            user_prompt: str = input("\nYour question: ")
            if user_prompt.lower() in ["q", "quit", "exit"]:
                print("Goodbye!")
                break

            # Run OpenAI agent
            result: AgentRunResult[str] = openai_agent.run_sync(user_prompt=user_prompt)
            print(f"\nOpenAI Agent: {result.output}")

            # Run ollama agent
            history_message: list[ModelRequest | ModelResponse] = result.new_messages()
            result: AgentRunResult[str] = ollama_agent.run_sync(
                user_prompt="Please continue the conversation.",
                message_history=history_message,
            )
            print(f"\nOllama Agent: {result.output}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
