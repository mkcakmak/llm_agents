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





