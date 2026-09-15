import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available MCP tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool(
                "calculate",
                {"expression": "25 * 4 + 10"}
            )

            print("\nCalculation result:")
            print(result.content)


if __name__ == "__main__":
    asyncio.run(main())