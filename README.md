# MCP Server with Server-Sent Events (SSE)

This project implements a Model Context Protocol (MCP) server with Server-Sent Events (SSE) support, allowing real-time communication between the server and clients.

## Features

- MCP server with tool and resource support
- Server-Sent Events (SSE) for real-time updates
- CORS middleware for cross-origin requests
- Built-in tools:
  - `add(a: int, b: int)`: Adds two numbers
  - `greeting://{name}`: Returns a personalized greeting

## Installation

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Running the Server

1. Start the server:
```bash
uvicorn server_sse:starlette_app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at:
- HTTP Server: http://localhost:8000
- SSE Endpoints: /mcp/sse and /sse
- Messages Endpoints: /mcp/messages and /messages

## Using the Client

### Python Client Example

Here's how to use the SSE client in Python:

```python
import requests
import json
from sseclient import SSEClient
import asyncio
import aiohttp
import logging

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.messages_url = f"{base_url}/mcp/messages"
        self.sse_url = f"{base_url}/mcp/sse"

    async def list_tools(self):
        """List all available tools from the MCP server."""
        try:
            introspection_message = {
                "type": "request",
                "action": "introspect",
                "data": {}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.messages_url, json=introspection_message) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return None
        except Exception as e:
            logging.error(f"Error listing tools: {e}")
            return None

    async def add_numbers(self, a: int, b: int):
        """Use the add tool to sum two numbers."""
        message = {
            "type": "request",
            "action": "execute",
            "tool": "add",
            "data": {"a": a, "b": b}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.messages_url, json=message) as response:
                return await response.json()

    async def get_greeting(self, name: str):
        """Get a personalized greeting."""
        message = {
            "type": "request",
            "action": "get",
            "resource": f"greeting://{name}",
            "data": {}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.messages_url, json=message) as response:
                return await response.json()
```

### Using the Client

```python
async def main():
    client = MCPClient()
    
    # List available tools
    tools = await client.list_tools()
    print("Available tools:", tools)
    
    # Add two numbers
    result = await client.add_numbers(5, 3)
    print("5 + 3 =", result)
    
    # Get a greeting
    greeting = await client.get_greeting("Alice")
    print(greeting)

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript/Browser Client Example

```javascript
// Connect to SSE stream
const eventSource = new EventSource('http://localhost:8000/mcp/sse');

// Listen for messages
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Send a message to execute the add tool
async function addNumbers(a, b) {
    const response = await fetch('http://localhost:8000/mcp/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: 'request',
            action: 'execute',
            tool: 'add',
            data: { a, b }
        })
    });
    return await response.json();
}

// Get a greeting
async function getGreeting(name) {
    const response = await fetch('http://localhost:8000/mcp/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: 'request',
            action: 'get',
            resource: `greeting://${name}`,
            data: {}
        })
    });
    return await response.json();
}
```

## API Documentation

### Tools

#### Add Tool
- Name: `add`
- Description: Add two numbers
- Parameters:
  - `a`: integer
  - `b`: integer
- Returns: integer (sum of a and b)

### Resources

#### Greeting Resource
- Pattern: `greeting://{name}`
- Description: Get a personalized greeting
- Parameters:
  - `name`: string
- Returns: string (personalized greeting message)

### Message Format

#### Request Format
```json
{
    "type": "request",
    "action": "execute|get|introspect",
    "tool": "tool_name",  // for execute
    "resource": "resource_pattern",  // for get
    "data": {
        // parameters
    }
}
```

#### Response Format
```json
{
    "type": "response",
    "data": {
        // response data
    }
}
```

## Error Handling

The server returns error responses with status code 500 and an error message:
```json
{
    "error": "Error message description"
}
```

## Logging

Server logs are written to both the console and `logs/server_sse.log`. The log level is set to DEBUG for detailed information 