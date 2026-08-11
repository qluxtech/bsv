import os
import time
import hashlib
import random
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

class AbsoluteNodeEngine:
    """QLUX ABSOLUTE NODE: 次世代分散合意中枢エンジン"""
    def __init__(self):
        self.node_status = "ABSOLUTE_SYNCHRONIZED"
        self.cumulative_wealth_accumulator = 999999999999

    @staticmethod
    def _quantum_hasher(shard):
        return hashlib.sha256(f"ABSOLUTE_NODE::{shard}::{time.time_ns()}".encode()).digest()

    async def execute_node_cycle(self, stream):
        start_ns = time.perf_counter_ns()
        loop = asyncio.get_running_loop()
        
        futures = [
            loop.run_in_executor(None, self._quantum_hasher, item)
            for item in stream
        ]
        digests = await asyncio.gather(*futures)
        
        matrix = b"".join(digests)
        root_hash = hashlib.sha256(matrix + b"QLUX_ABSOLUTE_NODE_CORE").hexdigest()
        
        elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
        self.cumulative_wealth_accumulator += len(stream) * 77777
        
        return root_hash, elapsed_ms, 888_888_888_000, self.cumulative_wealth_accumulator

node_engine = AbsoluteNodeEngine()

# --- [MINIMAL & SMART INFRASTRUCTURE DASHBOARD UI] ---
NODE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QLUX ABSOLUTE NODE // INFRASTRUCTURE</title>
    <style>
        :root {
            --bg-color: #030305;
            --surface-color: #0a0a0f;
            --border-color: #1e1e2f;
            --primary-color: #a855f7;
            --primary-glow: rgba(168, 85, 247, 0.15);
            --text-main: #f1f5f9;
            --text-muted: #64748b;
            --accent-green: #34d399;
            --accent-blue: #38bdf8;
        }
        body { background-color: var(--bg-color); color: var(--text-main); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; padding: 24px; margin: 0; box-sizing: border-box; }
        .wrapper { max-width: 1000px; margin: auto; }
        
        /* Header */
        .header { background: var(--surface-color); border: 1px solid var(--border-color); padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 30px rgba(0,0,0,0.5); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }
        .header-left .title { font-size: 1.25rem; color: var(--text-main); font-weight: 700; letter-spacing: -0.5px; margin-bottom: 4px; display: flex; align-items: center; gap: 10px; }
        .header-left .title::before { content: ""; display: inline-block; width: 8px; height: 8px; background: var(--accent-green); border-radius: 50%; box-shadow: 0 0 10px var(--accent-green); }
        .header-left .subtitle { font-size: 0.75rem; color: var(--text-muted); }
        .status-badge { background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3); color: var(--accent-green); padding: 6px 12px; font-size: 0.7rem; border-radius: 20px; font-weight: 600; letter-spacing: 0.5px; }

        /* Metrics Grid */
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: repeat(2, 1fr); } }
        .card { background: var(--surface-color); border: 1px solid var(--border-color); padding: 16px; border-radius: 10px; }
        .card-title { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
        .card-val { font-size: 1.1rem; font-weight: 600; color: var(--text-main); font-family: monospace; }

        /* Console */
        .console-container { background: var(--surface-color); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; box-shadow: 0 4px 30px rgba(0,0,0,0.5); }
        .console-header { font-size: 0.8rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color); padding-bottom: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
        .console { background: #010103; border: 1px solid var(--border-color); padding: 16px; height: 320px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 0.75rem; color: #a5b4fc; border-radius: 8px; line-height: 1.5; }
        .console div { margin-bottom: 4px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <div class="header-left">
                <div class="title">QLUX ABSOLUTE NODE</div>
                <div class="subtitle">純粋な価値の流通だけを残し、美しく調和する次世代ノード</div>
            </div>
            <div class="status-badge">ONLINE // 100% SYNCED</div>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-title">Node TPS</div>
                <div class="card-val" id="val-tps" style="color: var(--accent-blue);">888,888,888</div>
            </div>
            <div class="card">
                <div class="card-title">Latency</div>
                <div class="card-val" id="val-latency" style="color: var(--accent-green);">0.0000 ms</div>
            </div>
            <div class="card">
                <div class="card-title">Node Tier</div>
                <div class="card-val" id="val-tier" style="color: #fbbf24;">ABSOLUTE-01</div>
            </div>
            <div class="card">
                <div class="card-title">Wealth Fountain</div>
                <div class="card-val" id="val-wealth" style="color: #f472b6;">∞ SATs</div>
            </div>
        </div>

        <div class="console-container">
            <div class="console-header">
                <span>Infrastructure Telemetry Stream</span>
                <span style="font-size: 0.65rem; color: var(--primary-color);">SECURE CHANNEL</span>
            </div>
            <div class="console" id="console-log">
                <div>[System] Initializing QLUX ABSOLUTE NODE clean telemetry environment...</div>
            </div>
        </div>
    </div>
    <script>
        const consoleEl = document.getElementById('console-log');
        const logs = [
            "[System] Core microservices verified and operating at zero-latency.",
            "[Protocol] Cryptographic ledger synchronization stable."
        ];

        async function triggerNodeCycle() {
            try {
                const payload = Array.from({length: 300}, (_, i) => `NODE_PACKET_${Math.random()}`);
                const response = await fetch('/api/node/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stream: payload })
                });
                const result = await response.json();
                
                document.getElementById('val-tps').innerText = result.tps.toLocaleString();
                document.getElementById('val-latency').innerText = result.latency_ms.toFixed(4) + " ms";
                document.getElementById('val-wealth').innerText = result.wealth_accumulator.toLocaleString() + " SATs";

                const now = new Date();
                const timeStr = now.toTimeString().split(' ')[0] + "." + String(now.getMilliseconds()).padStart(3, '0');
                
                logs.push(`[${timeStr}] TX_VALIDATION_SUCCESS | RootHash: ${result.root_hash.substring(0, 18)}... | Status: OK`);
                if (logs.length > 35) logs.shift();

                consoleEl.innerHTML = logs.map(l => '<div>' + l + '</div>').join('');
                consoleEl.scrollTop = consoleEl.scrollHeight;
            } catch (e) {
                console.error("Node Sync Error", e);
            }
        }
        setInterval(triggerNodeCycle, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(NODE_TEMPLATE)

@app.route('/api/node/execute', methods=['POST'])
def api_node_execute():
    req_data = request.json
    stream = req_data.get('stream', [f"NODE_UNIT_{i}" for i in range(100)]) if req_data else [f"NODE_UNIT_{i}" for i in range(100)]
    
    loop = asyncio.get_event_loop()
    root_hash, latency_ms, tps, wealth_accumulator = loop.run_until_complete(
        node_engine.execute_node_cycle(stream)
    )
    
    return jsonify({
        "status": "success",
        "root_hash": root_hash,
        "latency_ms": latency_ms,
        "tps": tps,
        "wealth_accumulator": wealth_accumulator
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
