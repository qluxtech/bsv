import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# (V2ベースの安定版)
@app.route('/')
def home():
    return render_template_string("<h1>System Online: F-Kame Mesh Active</h1>")

@app.route('/ledger')
def ledger():
    return jsonify({"status": "active", "design": "F-Kame V2-V3 Hybrid"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000
