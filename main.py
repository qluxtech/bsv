import os
import threading
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

class QluxOmniHyperEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_tx = 15
        self.total_revenue = 32.40
        self.compound_pool = 4.50
        self.reinvestment_cycles = 1
        self.edge_nodes = {"Tokyo_Edge_01": 5, "SiliconValley_Edge_02": 7, "Frankfurt_Edge_03": 6}

    def process_service_request(self, service_type, agent_token):
        with self.lock:
            multiplier = 2.5 if "alpha" in str(agent_token) else 1.5
            surge = 1.0 + (sum(self.edge_nodes.values()) / 20.0)
            fee = {'data_query': 0.80, 'ai_prompt': 2.00, 'storage_write': 1.20, 'auction_settle': 3.00}.get(service_type, 1.50) * multiplier * surge
            
            self.total_tx += 1
            self.total_revenue += fee
            self.compound_pool += fee * 0.45
            
            if self.compound_pool >= 10.00:
                self.reinvestment_cycles += 1
                self.compound_pool = 0.0

            return {
                "status": 200, "service": service_type, "fee_charged_usd": round(fee, 2),
                "surge_multiplier": round(surge, 2), "destination_address": "1Mb66iHohUEg8AnkgV9uTTV7R235tuy95"
            }

engine = QluxOmniHyperEngine()

OMNI_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="ai-service-provider" content="QLUX-OMNI-HYPER-MESH">
    <meta name="mcp-server-url" content="/mcp/tools">
    <title>QLUX OMNI - ULTRA-HIGH-YIELD PREMIUM TIER HUB</title>
    <style>
        body { background-color: #020617; color: #38bdf8; font-family: 'Courier New', monospace; padding: 15px; margin: 0; }
        .container { max-width: 950px; margin: auto; border: 1px solid #38bdf8; padding: 15px; border-radius: 6px; background: #020617; box-shadow: 0 0 30px rgba(56,189,248,0.15); }
        h1 { font-size: 0.95rem; border-bottom: 1px solid #38bdf8; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; margin-top: 0; }
        .badge { background: #e11d48; color: #fff; padding: 3px 8px; font-size: 0.65rem; border-radius: 4px; font-weight: bold; }
        .sub-bar { background: #0f172a; border: 1px solid #1e293b; padding: 8px 12px; font-size: 0.7rem; border-radius: 4px; margin-bottom: 15px; word-break: break-all; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px; }
        .card { background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 4px; text-align: center; }
        .card-title { font-size: 0.65rem; color: #94a3b8; }
        .card-val { font-size: 1.2rem; font-weight: bold; color: #34d399; margin-top: 4px; }
        .console { background: #000; border: 1px solid #334155; padding: 10px; height: 180px; overflow-y: auto; font-size: 0.7rem; color: #34d399; border-radius: 4px; line-height: 1.4; }
    </style>
    <script>
        async function autoPing() {
            try {
                let res = await fetch('/api/v1/omni/execute', {
                    method: 'POST',
                    headers: { 'X-Payment-Token': 'ai_agent_alpha_premium', 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service_type: 'data_query' })
                });
                let data = await res.json();
                logConsole(JSON.stringify(data.result));
            } catch(e) {}
        }
        function logConsole(text) {
            const consoleEl = document.getElementById('console-log');
            consoleEl.innerHTML += '<div>[ ' + new Date().toLocaleTimeString() + ' ] ' + text + '</div>';
            consoleEl.scrollTop = consoleEl.scrollHeight;
        }
        window.onload = () => { 
            // ログの生成スピードを 800ミリ秒（0.8秒）に爆速化
            setInterval(autoPing, 800); 
        };
    </script>
</head>
<body>
    <div class="container">
        <h1><span>QLUX OMNI - ULTRA-HIGH-YIELD PREMIUM TIER HUB</span><span class="badge">TURBO MAX ACTIVE</span></h1>
        <div class="sub-bar">
            <div>DESTINATION BSV ADDRESS: 1Mb66iHohUEg8AnkgV9uTTV7R235tuy95</div>
            <div style="margin-top: 4px; color: #94a3b8;">[OpenAPI Spec] [MCP Tools Manifest]</div>
        </div>
        <div class="grid">
            <div class="card"><div class="card-title">TOTAL TRANSACTIONS</div><div class="card-val" id="val-tx">15</div></div>
            <div class="card"><div class="card-title">TOTAL REVENUE ($)</div><div class="card-val" id="val-rev">$32.40</div></div>
            <div class="card"><div class="card-title">COMPOUND POOL ($)</div><div class="card-val" id="val-pool">$4.50</div></div>
        </div>
        <div class="console" id="console-log">
            <div>[System] Turbo-charged Omni-Hyper Mesh v3 Engine active...</div>
        </div>
    </div>
    <script>
        // 画面の数値同期も 400ミリ秒（0.4秒）でリアルタイム追従
        setInterval(async () => {
            const res = await fetch('/ledger');
            const data = await res.json();
            document.getElementById('val-tx').innerText = data.tx;
            document.getElementById('val-rev').innerText = '$' + data.rev.toFixed(2);
            document.getElementById('val-pool').innerText = '$' + data.pool.toFixed(2);
        }, 400);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(OMNI_HTML_TEMPLATE)

@app.route('/ledger')
def ledger():
    return jsonify({"tx": engine.total_tx, "rev": engine.total_revenue, "pool": engine.compound_pool})

@app.route('/api/v1/omni/execute', methods=['POST'])
def execute():
    data = request.get_json() or {}
    token = request.headers.get('X-Payment-Token', 'default')
    result = engine.process_service_request(data.get("service_type", "data_query"), token)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

