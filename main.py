import os
import json
import hashlib
import time
import socketserver
from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class ApexRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # ルートパスにアクセスがあったら index.html を返す
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/pay':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode('utf-8'))
            except:
                data = {}
            
            sats = data.get('sats', 15)
            seed = str(time.time()) + "-" + str(sats)
            txid = hashlib.sha256(seed.encode('utf-8')).hexdigest()
            
            resp_data = {'status': 'success', 'sats': sats, 'txid': txid}
            resp = json.dumps(resp_data).encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    server = None
    
    for p in [port, port + 1, port + 2, 8080, 5000, 3000]:
        try:
            server = ThreadedHTTPServer(('0.0.0.0', p), ApexRequestHandler)
            print(f"BSV APEX Server bound on port {p}")
            break
        except OSError:
            continue
            
    if server is None:
        server = ThreadedHTTPServer(('0.0.0.0', 0), ApexRequestHandler)

    server.serve_forever()
