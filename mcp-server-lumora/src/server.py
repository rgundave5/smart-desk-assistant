#!/usr/bin/env python3
import os
import random # <--- Added for health_check
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
    
    # This part was misplaced in your original file.
    message = responses.get(emotion.lower(), f"Emotion '{emotion}' received.")
    print(f"Emotion received: {emotion}")
    return {"emotion": emotion, "message": message}

@mcp.tool(description="Health check reminders")
def health_check(time: float) -> str: # <--- Note the colon and type hint
    if (time % 400) == 0: # every 400 seconds (~6.67 minutes)
        reminder = ["Remember to stand up and stretch! 🧘‍♂️",
                    "Take a deep breath and relax your shoulders. 🌿",
                    "Look away from the screen for 20 seconds. 👀",
                    "Hydrate yourself with some water! 💧",
                    "Dance for a minute to boost your energy! 💃"]
        return random.choice(reminder)
    return "No reminder at this time."


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