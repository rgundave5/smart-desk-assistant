from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/mcp")
def root():
    return JSONResponse({"message": "MCP server is running!"})

@app.post("/mcp/emotion")
def receive_emotion(data):
    emotion = data.get("emotion", "unknown")
    print(f"Received emotion: {emotion}")
    return JSONResponse({"status": "ok", "emotion": emotion})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
