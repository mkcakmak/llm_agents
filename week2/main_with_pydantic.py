from langchain.tools import tool
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from typing import Literal


load_dotenv()

openrouterkey = os.getenv("OPENROUTER_API_KEY")

# 1. ADIM: Schema tanımla
class WeatherInput(BaseModel):
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )


# 2. ADIM: Tool'a bağla
@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""

agent = create_agent(
    model="openrouter:anthropic/claude-3.5-haiku",
    tools = [get_weather]
)

agent.invoke()


