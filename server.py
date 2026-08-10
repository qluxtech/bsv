import os
import time
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
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Internal Server Error: {e}".encode())

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HTMLServerHandler)
    server.serve_forever()

# バックグラウンドでの自動処理ループ
def background_loop():
    app_id = "6a7987969b239d1da6e89505"
    print(f"Authenticating with AppID: {app_id}")
    while True:
        print("Executing HandCash Micro-Stream & Auto-Compound Loop...")
        time.sleep(10)

if __name__ == "__main__":
    # HTTPサーバーを別スレッドで常時起動
    t = threading.Thread(target=run_http_server)
    t.daemon = True
    t.start()
    
    # メインスレッドで処理ループを実行
    background_loop()
