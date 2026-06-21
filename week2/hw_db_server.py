from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine,text, inspect
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("PG_DSN"))

mcp = FastMCP("Database")

@mcp.tool()
def list_tables() -> str:
    """List all table names in the database."""
    insp = inspect(engine)
    tables = insp.get_table_names()
    return "Tables: " + ", ".join(tables)


@mcp.tool()
def describe_table(table_name: str) -> str:
    """Describe the columns of a given table: name, type, and nullability."""
    insp = inspect(engine)
    columns = insp.get_columns(table_name)

    lines = []

    for col in columns :
        lines.append(f"{col['name']}({col['type']}, nullable = {col['nullable']})")

    return "\n".join(lines)

@mcp.tool()
def run_select(sql: str, max_rows: int = 50) -> str:
    """Execute a read-only SELECT statement and return results as a markdown table."""
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        if not rows:
            return "Query executed successfully, but returned 0 rows."

        col_names = result.keys()
        rows = rows[:max_rows]

    header = "| " + " | ".join(col_names) + " |"
    sep = "| " + " | ".join("---" for _ in col_names) + " |"
    body = ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]

    return "\n".join([header, sep] + body)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

