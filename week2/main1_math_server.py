from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:float, b:float) -> str:
    """Add two numbers together."""
    return f"{a} + {b} = {a+b}"

@mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtract b from a."""
    return f"{a} - {b} = {a - b}"
 
 
@mcp.tool()
def multiply(a: float, b: float) -> str:
    """Multiply two numbers."""
    return f"{a} * {b} = {a * b}"
 
 
@mcp.tool()
def divide(a: float, b: float) -> str:
    """Divide a by b."""
    if b == 0:
        return "Error: Division by zero is not allowed."
    return f"{a} / {b} = {a / b}"
 

@mcp.prompt()
def math_question_prompt(
    operation: str,
    a: float,
    b: float,
) -> str:
    """
    Generate a math question prompt.
    """
    return f"""
You are a mathematics assistant.

Solve the following operation and explain each step clearly.

Operation: {operation}
First number: {a}
Second number: {b}

Provide:
1. The calculation
2. The result
3. A short explanation
"""


if __name__ == "__main__":
    # stdio transport: client starts this as a subprocess and talks
    # to it over stdin/stdout — no network port involved.
    mcp.run(transport="stdio")


