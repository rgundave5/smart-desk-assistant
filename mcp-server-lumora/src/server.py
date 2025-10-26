#!/usr/bin/env python3
import os
from fastmcp import FastMCP

mcp = FastMCP("Lumora MCP Server")

@mcp.tool(description="Receive emotion data and respond with an appropriate message")
def process_emotion(emotion: str) -> dict:
    responses = {
        "tired": "Time for a break 😴",
        "focused": "Keep it up 💪",
        "stressed": "Take a deep breath 🌿",
        "happy": "Love that energy 🌞",
    }

    message = responses.get(emotion.lower(), f"Emotion '{emotion}' received.")
    print(f"Emotion received: {emotion}")
    return {"emotion": emotion, "message": message}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    print(f"Starting FastMCP server on {host}:{port}")

    # Use FastMCP’s built-in CLI listing to confirm tools
    print("✅ MCP server initialized. Visit /mcp to confirm it’s running.")
    print("Try calling /tools/process_emotion with curl.")

    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
