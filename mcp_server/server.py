from fastmcp import FastMCP


mcp = FastMCP("AgentFlow MCP Server")


@mcp.tool()
def calculate(expression: str) -> str:
    """
    Evaluate a basic mathematical expression.

    Example:
    calculate("25 * 4")
    """

    try:
        allowed_characters = set(
            "0123456789+-*/().% "
        )

        if not all(
            character in allowed_characters
            for character in expression
        ):
            return "Invalid mathematical expression."

        result = eval(expression, {"__builtins__": {}}, {})

        return str(result)

    except Exception:
        return "Unable to calculate the expression."


if __name__ == "__main__":
    mcp.run()