import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


load_dotenv()


model =  init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    max_tokens=500
)

async def main():
    client = MultiServerMCPClient({
        "database" : {
            "transport" : "streamable-http",
            "url": "http://localhost:8000/mcp"
        }
    })


    tools = await client.get_tools()
    print("Tools loaded:", [t.name for t in tools])

    agent = create_agent(
        model=model,
        tools = tools,
        system_prompt=    "You are a database assistant. You must ALWAYS call list_tables and "
    "describe_table on every relevant table BEFORE calling run_select. "
    "Never guess table or column names. "
    "In SQL, use single quotes for string literals (e.g. WHERE name = 'Engineering'), "
    "never double quotes for values."

    )

    response = await agent.ainvoke({
        "messages": [
            {"role" : "user",
             "content": "Give me the name of the employee who has highest salary and works in engineering department"}
        ]
    })

    for msg in response["messages"]:
        msg.pretty_print()

if __name__ == "__main__":
    asyncio.run(main())