import http.server
import socketserver
import json
import time
import threading
import os

# Renderの動的ポートを確実に取得
PORT = int(os.environ.get("PORT", 10000))
BSV_MAINNET_ADDRESS = "1Mb66iHohUEg8AnkgV9uTTV7R235tuy95"

class QluxOmniEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_tx = 0
        self.total_revenue = 0.0
        self.compound_pool = 0.0
        self.reinvestment_cycles = 0
        self.edge_nodes = {"Tokyo_Edge_01": 1, "SiliconValley_Edge_02": 1, "Frankfurt_Edge_03": 1}

    def process(self, service_type, token):
        with self.lock:
            multiplier = 2.5 if "alpha" in str(token) else 1.5
            surge = 1.0 + (sum(self.edge_nodes.values()) / 50.0)
            fee = {'data_query': 0.80, 'ai_prompt': 2.00, 'storage_write': 1.20, 'auction_settle': 3.00}.get(service_type, 1.50) * multiplier * surge
            
            self.total_tx += 1
            self.total_revenue += fee
            self.compound_pool += fee * 0.45
            
            if self.compound_pool >= 10.00:
                self.reinvestment_cycles += 1
                self.compound_pool = 0.0

            return {
                "status": 200,
                "service": service_type,
                "fee_charged_usd": round(fee, 2),
                "surge_multiplier": round(surge, 2),
                "destination_address": BSV_MAINNET_ADDRESS
            }

engine = QluxOmniEngine()

HTML_PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="ai-service-provider" content="QLUX-OMNI-HYPER-MESH">
    <meta name="mcp-server-url" content="/mcp/tools">
    <title>QLUX OMNI - HYPER-YIELD SURGE MESH</title>
    <style>
        body { background-color: #020617; color: #38bdf8; font-family: 'Courier New', monospace; padding: 20px; }
        .container { max-width: 900px; margin: auto; border: 1px solid #38bdf8; padding: 20px; border-radius: 8px; box-shadow: 0 0 40px rgba(56,189,248,0.2); }
        h1 { font-size: 1.1rem; border-bottom: 1px solid #38bdf8; padding-bottom: 8px; display: flex; justify-content: space-between; }
        .badge { background: #e11d48; color: #fff; padding: 2px 8px; font-size: 0.7rem; border-radius: 4px; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px; }
        .card { background: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 6px; text-align: center; }
        .card-val { font-size: 1.4rem; font-weight: bold; color: #34d399; margin-top: 5px; }
        .console { background: #000; border: 1px solid #334155; padding: 12px; margin-top: 20px; height: 220px; overflow-y: auto; font-size: 0.75rem; color: #34d399; }
    </style>
    <script>
        async function autoPing() {
            try {
                await fetch('/api/v1/omni/execute', {
                    method: 'POST',
                    headers: { 'X-Payment-Token': 'ai_agent_alpha_premium' },
                    body: JSON.stringify({ service_type: 'data_query' })
                });
            } catch(e) {}
        }
        window.onload = () => { autoPing(); setInterval(autoPing, 3000); };
    </script>
</head>
<body>
    <div class="container">
        <h1><span>QLUX OMNI - SURGE MESH HUB</span><span class="badge">LIVE ACTIVE</span></h1>
        <div class="grid">
            <div class="card"><div>TOTAL TRANSACTIONS</div><div class="card-val" id="val-tx">0</div></div>
            <div class="card"><div>TOTAL REVENUE ($)</div><div class="card-val" id="val-rev">$0.00</div></div>
        </div>
        <div class="console" id="log">System initialized. Awaiting autonomous AI traffic...</div>
    </div>
    <script>
        setInterval(async () => {
            const res = await fetch('/ledger');
            const data = await res.json();
            document.getElementById('val-tx').innerText = data.tx;
            document.getElementById('val-rev').innerText = '$' + data.rev.toFixed(2);
        }, 1500);
    </script>
</body>
</html>
"""

class ServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if "ledger" in self.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"tx": engine.total_tx, "rev": engine.total_revenue}).encode('utf-8'))
        elif "mcp/tools" in self.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"mcp_version": "2026-02", "tools": [{"name": "qlux_execute"}]}).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode('utf-8')) if length > 0 else {}
        result = engine.process(data.get("service_type", "data_query"), self.headers.get('X-Payment-Token'))
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"result": result}).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ServerHandler) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()
