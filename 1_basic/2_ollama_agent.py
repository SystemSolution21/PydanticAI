from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


class ContentSummary(BaseModel):
    title: str
    summary: str


# Create ollama model
ollama_model = OpenAIModel(
    model_name="llama3.2:3b",
    provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
)

# Create ollama agent
ollama_agent = Agent(
    model=ollama_model,
    output_type=ContentSummary,
    instructions="You are a helpful assistant. Summarize the content and return the title and summary.",
)

# Main entrypoint
if __name__ == "__main__":
    while True:
        try:
            user_prompt: str = input("\nAsk any question (type 'q' to quit): ")
            if user_prompt.lower() in "q":
                print("Goodbye!")
                break

            result: AgentRunResult[ContentSummary] = ollama_agent.run_sync(
                user_prompt=user_prompt
            )
            print(f"\nOllama Agent: {result.output}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break
