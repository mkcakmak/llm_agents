from dotenv import load_dotenv
from langchain.agents import create_agent
import os

load_dotenv()

openrouterkey = os.getenv("OPENROUTER_API_KEY")

def get_weather(city) :
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def get_time(city):
    """Get the current local time for a given city."""
    return f"The local time in {city} is 14:30."

def convert_currency(amount, rate):
    """Convert an amount using a given exchange rate."""
    result = amount * rate
    return f"{amount} converted at rate {rate} equals {result}."

tools1 = [get_weather, get_time]


agent1 = create_agent(
    model="openrouter:anthropic/claude-3.5-haiku",
    tools=tools1,
    system_prompt="You are a helpful assistant",
)

result1 = agent1.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in Zurich and what time is it there?"}]}
)

tools2 = [convert_currency]

agent2 = create_agent(
    model="openrouter:anthropic/claude-3.5-haiku",
    tools=tools2,
    system_prompt="You are a helpful assistant",
)

result2 = agent2.invoke(
    {"messages": [{"role": "user", "content": "I have 100 euros and the rate is 1.08 — how many dollars is that?"}]}
)

print(result1["messages"][-1].content)
print(result2["messages"][-1].content)
