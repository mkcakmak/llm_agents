from dotenv import load_dotenv
from langchain.agents import create_agent
import os

load_dotenv()

def get_weather(city):
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def get_time(city):
    """Get the current local time for a given city."""
    return f"The local time in {city} is 14:30."

def convert_currency(amount, rate):
    """Convert an amount using a given exchange rate."""
    result = amount * rate
    return f"{amount} converted at rate {rate} equals {result}."


class HomeworkAgent:
    def __init__(self):
        self.tools = [get_weather, get_time, convert_currency]
        self.agent = create_agent(
            model="openrouter:anthropic/claude-3.5-haiku",
            tools=self.tools,
            system_prompt="You are a helpful assistant",
        )

    def ask(self, question):
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        return result["messages"]


agent = HomeworkAgent()

print("=== Task 1 ===")
print(agent.ask("What's the weather and local time in Istanbul?"))

print("\n=== Task 2 ===")
print(agent.ask("I have 100 euros and the rate is 1.08 — how many dollars is that?"))