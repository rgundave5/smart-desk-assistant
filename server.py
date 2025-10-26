from flask import Flask, request, jsonify

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

if __name__ == "__main__":
    app.run(debug=True, port=8000)

    