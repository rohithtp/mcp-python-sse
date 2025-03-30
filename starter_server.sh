#!/bin/bash

# Activate the virtual environment created by uv
source .venv/bin/activate

# Start the MCP server
# This server provides:
# 1. An addition tool that adds two numbers
# 2. A dynamic greeting resource at /greeting/{name}
python server.py 