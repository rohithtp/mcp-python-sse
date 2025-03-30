from mcp.server.fastmcp import FastMCP
import logging
import sys
import os
import traceback

# Create an MCP server
mcp = FastMCP("Demo")

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
                logging.FileHandler('logs/server.log')
            ]
        )
        
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        for handler in logger.handlers:
            handler.flush()
        
        print("Starting server with logging enabled...")
        logger.info("Starting MCP Demo server...")
        logger.info("Available endpoints:")
        logger.info("  - Tool: add(a: int, b: int)")
        logger.info("  - Resource: /greeting/{name}")
        
        logger.info("WebSocket Details:")
        logger.info("  - WebSocket URL: ws://localhost:8765/ws")
        logger.info("  - HTTP Server: http://localhost:8765")
        logger.info("  - WebSocket Path: /ws")
        logger.info("  - Protocol: WebSocket (ws://)")
        logger.info("Connection Instructions:")
        logger.info("  1. Connect to the WebSocket endpoint at ws://localhost:8765/ws")
        logger.info("  2. Use the MCP client library for proper protocol handling")
        logger.info("  3. Example client connection: websocket_client('ws://localhost:8765/ws')")

        for handler in logger.handlers:
            handler.flush()
            
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
    
    try:
        print("Starting MCP server...")
        mcp.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {str(e)}")
        traceback.print_exc() 