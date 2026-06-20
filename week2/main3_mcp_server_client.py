import asyncio
import os
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# Initialize the model
model = init_chat_model(
    model="gemini-2.5-flash", 
    model_provider="google_genai", 
    max_tokens=300
)

async def demonstrate_multi_server_mcp():
    """Demonstrate connecting to multiple MCP servers with different transports."""
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    math_server_path = script_dir / "main1_math_server.py"
    search_server_path = script_dir / "main_search_server.py"
    
    # Configure multiple MCP servers with different transports
    client = MultiServerMCPClient({
        # local math server using stdio transport
        "math" :{
            "transport" : "stdio",
            "command" : "python",
            "args" : [str(math_server_path)]
        },

        # local search/utility server using stdio transport
        "search": {
            "transport": "stdio",
            "command": "python",
            "args": [str(search_server_path)],
        },

        # remote weather server using http transport
        "weather" : {
            "transport" : "streamable-http",
            "url" : "http://localhost:8000/mcp"
        }
    })

    # --- TOOLS: math + search + weather tools, all merged into one list ---
    tools = await client.get_tools()
   
    # --- RESOURCE: only defined on the weather server ---
    resources = await client.get_resources("weather")

    condition_guide = next(
        r for r in resources if "current-conditions-guide" in str(r.metadata.get("uri", ""))
    )
    guide_text = condition_guide.data

    history = await client.get_resources("weather", uris = ["weather://history/Tokyo"])
    history_text = history[0].data

    # --- PROMPT: weather-specific template, from the weather server ---
    weather_prompt_messages= await client.get_prompt(
        server_name="weather",
        prompt_name="weather_report_prompt",
        arguments={"location": "Tokyo",
                   "tone" : "casual"},
    )

    # --- PROMPT: generic template, from the search server ---
    general_prompt_messages = await client.get_prompt(
        server_name="search",
        prompt_name="general_question_prompt",
        arguments = {
            "topic": "2026 NATO zirvesi hangi ülkede olacak",
            "tone" : "casual",
        },
    )


    prompt_messages = await client.get_prompt(
    server_name="math",
    prompt_name="math_question_prompt",
    arguments={
        "operation": "multiply",
        "a": "12",
        "b": "8",
    },
)

    agent = create_agent(
        model = model,
        tools= tools, # math + search + weather, all together
        system_prompt=(
            "You are a helpful assistant with access to math, "
            "search, and weather tools.\n\n"
            f"Weather reference guide:\n{guide_text}\n\n"
            f"Historical context:\n{history_text}"
        )
    )

    # Pick ONE of the two prompt-generated message sets to send.
    # Here we use the general/NATO question.
    response = await agent.ainvoke({"messages": prompt_messages})

    print(f"Result: {response}")


if __name__=='__main__':
    asyncio.run(demonstrate_multi_server_mcp())