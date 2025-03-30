from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.background import BackgroundTask
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import logging
import sys
import os
import traceback
import asyncio
import json
from typing import List, Dict

# Create an MCP server
mcp = FastMCP("Demo")

# Store active SSE connections
connections: List[asyncio.Queue] = []

async def stream_events(queue: asyncio.Queue):
    while True:
        try:
            message = await queue.get()
            if message is None:  # Connection close signal
                break
            yield f"data: {json.dumps(message)}\n\n"
        except Exception as e:
            logging.error(f"Error in stream_events: {e}")
            break

# SSE handlers
async def handle_sse(request: Request):
    queue = asyncio.Queue()
    connections.append(queue)
    
    async def cleanup():
        if queue in connections:
            connections.remove(queue)
            await queue.put(None)
    
    return Response(
        content=stream_events(queue),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
        background=BackgroundTask(cleanup)
    )

async def handle_messages(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received message: {data}")
        
        # Handle the message based on its type
        if data.get("type") == "request" and data.get("action") == "introspect":
            # Handle introspection request
            response = {
                "type": "response",
                "data": {
                    "tools": [
                        {
                            "name": "add",
                            "description": "Add two numbers",
                            "parameters": {
                                "a": {"type": "integer"},
                                "b": {"type": "integer"}
                            },
                            "returns": {"type": "integer"}
                        }
                    ],
                    "resources": [
                        "greeting://{name}"
                    ]
                }
            }
        else:
            # Handle tool execution request
            response = await mcp.process_request(data)
        
        logging.info(f"Generated response: {response}")
        
        # Broadcast response to all connected clients
        for queue in connections:
            await queue.put(response)
        
        return JSONResponse(response)
    except Exception as e:
        logging.error(f"Error in handle_messages: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        error_response = {"error": str(e)}
        return JSONResponse(error_response, status_code=500)

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Create Starlette application with CORS middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# Create routes including the MCP-specific paths
routes = [
    Mount("/mcp", routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]),
    # Also keep root paths for compatibility
    Route("/sse", endpoint=handle_sse),
    Route("/messages", endpoint=handle_messages, methods=["POST"]),
]

app = Starlette(routes=routes, middleware=middleware)
starlette_app = app

if __name__ == "__main__":
    try:
        # Ensure the logs directory exists
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Configure logging with both file and terminal output
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('logs/server_sse.log')
            ]
        )
        
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        print("Starting server with logging enabled...")
        logger.info("Starting MCP Demo server with SSE...")
        logger.info("Available endpoints:")
        logger.info("  - Tool: add(a: int, b: int)")
        logger.info("  - Resource: /greeting/{name}")
        
        logger.info("SSE Server Details:")
        logger.info("  - HTTP Server: http://localhost:8000")
        logger.info("  - SSE Endpoints: /mcp/sse and /sse")
        logger.info("  - Messages Endpoints: /mcp/messages and /messages")
        logger.info("\nMCP Inspector Connection:")
        logger.info("  - Use URL: http://localhost:8000 in the MCP Inspector")

        # Start the server
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {str(e)}")
        traceback.print_exc() 