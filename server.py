# from flask import Flask, request, jsonify
# import sqlite3
# import pandas as pd

# app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def index():
    #return {"message": "Welcome! Flask server is running."}


#@app.route("/mcp", methods=["GET"])
#def home():
    #return {"message": "Flask MCP server running!"}

#@app.route("/mcp/emotion", methods=["POST"])
#def receive_emotion():
    #data = request.get_json()
    #print("Emotion received:", data)
    #return jsonify({"status": "ok", "emotion": data.get("emotion")})

#@app.route("/api/events")
#def get_events():
    #conn = sqlite3.connect("/path/to/tracker.db")
    #df = pd.read_sql_query("SELECT * FROM events", conn)
    #conn.close()
    #events = df.to_dict(orient="records")
    #return jsonify({"events": events})

#if __name__ == "__main__":
    #app.run(debug=True, port=8000)


# server.py
from flask import Flask, request, jsonify
import mcp_helper

from db import engine, Base
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route("/mcp", methods=["POST"])
def mcp():
    data = request.get_json(force=True)
    method = data.get("method")
    params = data.get("params", {})
    request_id = data.get("id")
    try:
        result = mcp_helper.handle_method(method, params)
        return jsonify({"jsonrpc": "2.0", "result": result, "id": request_id})
    except Exception as e:
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": request_id})

if __name__ == "__main__":
    app.run(debug=True)


    

    