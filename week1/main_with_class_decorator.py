from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
import os

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_time(city: str) -> str:
    """Get the current local time for a given city."""
    return f"The local time in {city} is 14:30."

@tool
def convert_currency(amount: float, rate: float) -> str:
    """Convert an amount using a given exchange rate."""
    result = amount * rate
    return f"{amount} converted at rate {rate} equals {result}."


agent = create_agent(
    model="openrouter:anthropic/claude-3.5-haiku",
    tools=[get_weather, get_time, convert_currency],
    system_prompt="You are a helpful assistant",
)

print("=== Task 1 ===")
result1 = agent.invoke({"messages": [{"role": "user", "content": "What's the weather and local time in Istanbul?"}]})
print(result1["messages"])

print("\n=== Task 2 ===")
result2 = agent.invoke({"messages": [{"role": "user", "content": "I have 100 euros and the rate is 1.08 — how many dollars is that?"}]})
print(result2["messages"])