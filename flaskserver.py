from flask import Flask, request, jsonify
import mcp_helper  # The MCP helper functions

from db import engine, Base
Base.metadata.create_all(engine)  # Ensure DB tables are created

app = Flask(__name__)

@app.route("/mcp", methods=["POST"])
def mcp():
    # Get the raw JSON-RPC request payload
    data = request.get_json(force=True)
    method = data.get("method")          # MCP method name
    params = data.get("params", {})      # MCP parameters dict
    request_id = data.get("id")          # Request id for response

    try:
        # Delegate processing to your MCP helper dispatcher
        result = mcp_helper.handle_method(method, params)
        # Return result in proper JSON-RPC 2.0 format
        return jsonify({"jsonrpc": "2.0", "result": result, "id": request_id})
    except Exception as e:
        # Handle errors and return JSON-RPC error object
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": str(e)},
            "id": request_id
        })

if __name__ == "__main__":
    app.run(debug=True)
