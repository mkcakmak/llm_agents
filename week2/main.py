
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from models import WeatherInput
from dotenv import load_dotenv
import json

load_dotenv()

model = init_chat_model(model="gemini-2.5-flash-lite", model_provider="google_genai", max_tokens=500)
agent= create_agent()

@tool
def search_database(query:str, limit:int= 10) -> str:
    """Search for customer database for relevant information.
    Args:
        query : "Search terms to look for"
        limit : "Maximum number of results to return
    
    """
    customers = ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Wilson"]
    matches = [c for c in customers if query.lower() in c.lower()][:limit]
    return f"Found {len(matches)} matches: {', '.join(matches)}"