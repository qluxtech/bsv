import os
import time
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# HTMLファイルを返すようにしたHTTPサーバー
class HTMLServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # ルート (/) にアクセスされたら index.html を表示
            file_path = "index.html" if self.path == "/" else self.path.lstrip("/")
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                if file_path.endswith(".html"):
                    self.send_header("Content-Type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(f"Internal Server Error: {e}".encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            auth_token = data.get('authToken')
            
            url = "https://cloud.handcash.io/v3/connect/payments"
            payload = {
                "instrumentCurrencyCode": "BSV",
                "denominationCurrencyCode": "USD",
                "receivers": [
                    {
                        "destination": "受取人のハンドル名またはpaymail",
                        "sendAmount": 0.01
                    }
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "authorization": f"Bearer {auth_token}"
            }
            
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "result": result}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HTMLServerHandler)
    server.serve_forever()

# バックグラウンドでの自動巡回ループ
def background_loop():
    app_id = "6a7987969b239d1d36e89505"
    print(f"Authenticating with AppID: {app_id}")
    while True:
        print("Executing HandCash Micro-Stream & Auto-Compound Loop...")
        time.sleep(10)

if __name__ == "__main__":
    # HTTPサーバーを別スレッドで同時起動
    t = threading.Thread(target=run_http_server)
    t.daemon = True
    t.start()

    # メインスレッドで巡回ループを実行
    background_loop()
