from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/dispatch', methods=['POST'])
def dispatch():
    req_data = request.json.get('data', 'QLUX_DEFAULT')
    # ここにブロックチェーン送金やAPI処理のロジックが入ります
    return jsonify({
        "success": True,
        "txId": "7a9f8b2c4e1d3f6a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

