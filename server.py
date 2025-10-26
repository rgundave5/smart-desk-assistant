from flask import Flask, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return {"message": "Welcome! Flask server is running."}


@app.route("/mcp", methods=["GET"])
def home():
    return {"message": "Flask MCP server running!"}

@app.route("/mcp/emotion", methods=["POST"])
def receive_emotion():
    data = request.get_json()
    print("Emotion received:", data)
    return jsonify({"status": "ok", "emotion": data.get("emotion")})

@app.route("/api/events")
def get_events():
    conn = sqlite3.connect("/path/to/tracker.db")
    df = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    events = df.to_dict(orient="records")
    return jsonify({"events": events})

if __name__ == "__main__":
    app.run(debug=True, port=8000)

    