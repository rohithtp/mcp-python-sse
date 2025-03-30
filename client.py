import asyncio
from mcp.client.websocket import websocket_client

async def main():
    # Create an MCP client
    async with websocket_client("ws://localhost:8765/ws") as client:
        # List all available tools
        tools = await client.list_tools()
        print("\nAvailable Tools:")
        for tool in tools.tools:
            print(f"\nTool: {tool.name}")
            print(f"Description: {tool.description}")
            print("Parameters:")
            for param in tool.parameters:
                print(f"  - {param.name}: {param.type}")
        
        # List all available resources
        resources = await client.list_resources()
        print("\nAvailable Resources:")
        for resource in resources.resources:
            print(f"\nResource: {resource.name}")
            print(f"Description: {resource.description}")

        # Test the add tool
        result = await client.invoke_tool("add", {"a": 5, "b": 3})
        print(f"\nAdd result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 