import os
import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_CODE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX APEX - Enterprise On-Chain Exchange</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
body { background-color: #000205; color: #ffffff; font-family: sans-serif; }
.card { background: rgba(8, 14, 28, 0.95); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 20px; padding: 24px; }
.swipe-box { position: relative; width: 100%; height: 75px; background: rgba(255,255,255,0.05); border-radius: 18px; border: 1px solid #f59e0b; overflow: hidden; user-select: none; }
.swipe-btn { position: absolute; left: 4px; top: 4px; width: 67px; height: 67px; background: #f59e0b; border-radius: 14px; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold; cursor: pointer; transition: background 0.2s; z-index: 10; }
.swipe-btn.unlocked { background: #10b981; color: #fff; }
.swipe-text { position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; color: #fbbf24; letter-spacing: 0.1em; }
</style>
</head>
<body class="min-h-screen p-4 sm:p-8">

<div class="max-w-4xl mx-auto space-y-6">
    <div class="card text-center">
        <h1 class="text-2xl sm:text-3xl font-black text-amber-400 mb-2">QLUX APEX ON-CHAIN HUB</h1>
        <p class="text-sm text-slate-400">AI & Enterprise High-Value Data & Nano-Payment Gateway</p>
    </div>

    <div class="card space-y-4">
        <h2 class="text-lg font-bold text-amber-400">Teranode AI Telemetry Stream</h2>
        <div class="bg-black/80 border border-cyan-500/30 rounded-xl p-4 font-mono text-xs space-y-2">
            <div class="text-cyan-400 font-bold">[LIVE FEED: ACTIVE]</div>
            <div class="text-slate-300">Active AI Swarm Consumers: <span class="text-amber-400">14,892 Nodes</span></div>
            <div class="text-slate-300">Throughput Velocity: <span class="text-emerald-400">1,420,000 TPS</span></div>
        </div>

        <div>
            <label class="block text-xs font-bold text-amber-400 mb-1">AI Agent Handle ID</label>
            <input type="text" id="user-handle" value="$qlux_ai_agent" class="w-full bg-black border border-white/20 rounded-lg px-3 py-2 text-white font-mono text-sm">
        </div>

        <div id="terminal" class="bg-black border border-cyan-500/50 rounded-xl p-4 font-mono text-xs hidden">
            <div class="text-cyan-400 font-bold mb-1">DATA UNLOCKED SUCCESSFULLY</div>
            <div id="terminal-body" class="text-slate-300 break-all"></div>
        </div>
    </div>

    <div class="card space-y-4">
        <h3 class="text-md font-bold text-white">Swipe Nano-Payment (15 Sats)</h3>
        <div class="swipe-box" id="swipe-container">
            <div class="swipe-text" id="swipe-text">SWIPE RIGHT TO PAY & UNLOCK &rarr;</div>
            <div class="swipe-btn" id="swipe-btn">&rarr;</div>
        </div>
    </div>
</div>

<script>
const container = document.getElementById('swipe-container');
const btn = document.getElementById('swipe-btn');
const text = document.getElementById('swipe-text');

let dragging = false;
let startX = 0;
let currentX = 0;
let maxDist = 0;

function getMax() {
    maxDist = container.clientWidth - btn.clientWidth - 8;
}
window.addEventListener('resize', getMax);
window.addEventListener('load', getMax);

btn.addEventListener('mousedown', e => {
    dragging = true;
    startX = e.clientX - currentX;
    text.style.opacity = '0.3';
});

window.addEventListener('mousemove', e => {
    if (!dragging) return;
    getMax();
    currentX = e.clientX - startX;
    if (currentX < 0) currentX = 0;
    if (currentX > maxDist) currentX = maxDist;
    btn.style.transform = 'translateX(' + currentX + 'px)';
});

window.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    getMax();
    if (currentX >= maxDist * 0.8) {
        btn.style.transform = 'translateX(' + maxDist + 'px)';
        btn.classList.add('unlocked');
        btn.innerHTML = 'OK';
        pay();
    } else {
        currentX = 0;
        btn.style.transform = 'translateX(0px)';
        text.style.opacity = '1';
    }
});

async function pay() {
    const handle = document.getElementById('user-handle').value;
    const term = document.getElementById('terminal');
    const body = document.getElementById('terminal-body');
    
    term.style.display = 'block';
    body.innerHTML = 'Broadcasting nano-payment to Teranode...';

    try {
        const res = await fetch('/api/pay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ handle: handle, sats: 15 })
        });
        const data = await res.json();
        
        setTimeout(() => {
            btn.classList.remove('unlocked');
            btn.innerHTML = '&rarr;';
            currentX = 0;
            btn.style.transform = 'translateX(0px)';
            text.style.opacity = '1';
            body.innerHTML = 'Handle: ' + data.handle + '<br>Amount: ' + data.sats + ' SATS<br>TXID: ' + data.txid + '<br><b class="text-emerald-400">[UNLOCKED] Data stream active.</b>';
        }, 400);
    } catch (e) {
        body.innerHTML = 'Error connecting to payment gateway.';
    }
}
</script>
</body>
</html>
"""

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            payload = HTML_CODE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/pay':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode('utf-8'))
            except:
                data = {}
            
            handle = data.get('handle', '$qlux')
            sats = data.get('sats', 15)
            txid = hashlib.sha256(f"{handle}-{sats}-{time.time()}".encode()).hexdigest()
            
            resp = json.dumps({'status': 'success', 'handle': handle, 'sats': sats, 'txid': txid}).encode('utf-8')
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
    server = HTTPServer(('0.0.0.0', port), SimpleServer)
    print(f"Server started on port {port}")
    server.serve_forever()
