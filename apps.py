from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/api/emotion-results")
def emotion_results():
    try:
        df = pd.read_csv("emotion_results.csv")  # or query DB instead
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)