import requests
import json
from sseclient import SSEClient
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.messages_url = f"{base_url}/mcp/messages"
        self.sse_url = f"{base_url}/mcp/sse"

    async def list_tools(self):
        """List all available tools from the MCP server."""
        try:
            # Send an introspection message to get tool information
            introspection_message = {
                "type": "request",
                "action": "introspect",
                "data": {}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.messages_url, json=introspection_message) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", {})
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to get tools. Status code: {response.status}")
                        logger.error(f"Error response: {error_text}")
                        return None
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return None

async def main():
    client = MCPClient()
    
    # Get and display tools
    tools_info = await client.list_tools()
    if tools_info:
        print("\nAvailable MCP Tools and Resources:")
        print("=" * 40)
        
        # Print tools
        if "tools" in tools_info:
            print("\nTools:")
            for tool in tools_info["tools"]:
                print(f"- {tool}")
        
        # Print resources
        if "resources" in tools_info:
            print("\nResources:")
            for resource in tools_info["resources"]:
                print(f"- {resource}")
    else:
        print("Failed to retrieve tools information")

if __name__ == "__main__":
    asyncio.run(main()) 