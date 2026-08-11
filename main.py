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

from flask import Flask, jsonify, render_template_string, request, redirect, url_for

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

# --- [QLUX ABSOLUTE NODE DASHBOARD UI WITH NAVIGATION BUTTONS] ---
NODE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QLUX ABSOLUTE NODE</title>
    <style>
        body { background-color: #000000; color: #a855f7; font-family: 'Courier New', monospace; padding: 14px; margin: 0; box-sizing: border-box; }
        .wrapper { max-width: 1200px; margin: auto; }
        .header { border: 2px solid #a855f7; background: #13021f; padding: 22px; border-radius: 8px; text-align: center; margin-bottom: 18px; box-shadow: 0 0 140px rgba(168,85,247,0.45); }
        .title { font-size: 1.5rem; color: #c084fc; font-weight: bold; letter-spacing: 3px; margin-bottom: 6px; }
        .subtitle { font-size: 0.72rem; color: #cbd5e1; }
        .feed-bar { background: #000000; border: 1px solid #581c87; padding: 8px; font-size: 0.62rem; margin-top: 10px; text-align: left; color: #e9d5ff; border-radius: 4px; word-break: break-all; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 18px; }
        @media (max-width: 768px) { .grid { grid-template-columns: repeat(2, 1fr); } }
        .card { background: #05030a; border: 1px solid #581c87; padding: 12px; border-radius: 8px; text-align: center; box-shadow: 0 0 20px rgba(168,85,247,0.2); }
        .card-title { font-size: 0.58rem; color: #cbd5e1; }
        .card-val { font-size: 1.1rem; font-weight: bold; color: #c084fc; margin-top: 6px; }
        
        /* GLOBAL SYNCHRONIZATION GRID */
        .sync-section { border: 2px solid #581c87; background: #07030f; padding: 15px; border-radius: 8px; margin-bottom: 18px; text-align: center; box-shadow: 0 0 30px rgba(168,85,247,0.15); }
        .sync-title { font-size: 0.85rem; color: #c084fc; font-weight: bold; margin-bottom: 4px; letter-spacing: 2px; }
        .sync-sub { font-size: 0.6rem; color: #94a3b8; margin-bottom: 14px; }
        .sync-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
        @media (max-width: 768px) { .sync-grid { grid-template-columns: repeat(2, 1fr); } }
        .sync-btn { background: #0d061c; border: 1px solid #7e22ce; color: #e9d5ff; padding: 12px 8px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 0.7rem; font-weight: bold; cursor: pointer; transition: all 0.2s ease; text-decoration: none; display: block; }
        .sync-btn:hover { background: #7e22ce; color: #fff; box-shadow: 0 0 15px rgba(168,85,247,0.8); transform: translateY(-2px); }
        .sync-btn.active-omega { border: 2px solid #c084fc; box-shadow: 0 0 20px rgba(192,132,252,0.6); }

        .console-container { border: 2px solid #a855f7; background: #090414; padding: 15px; border-radius: 8px; box-shadow: 0 0 100px rgba(168,85,247,0.3); }
        .console-header { font-size: 0.85rem; border-bottom: 1px solid #a855f7; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; color: #f8fafc; margin-bottom: 10px; }
        .badge { background: linear-gradient(135deg, #a855f7, #7e22ce); color: #fff; padding: 3px 8px; font-size: 0.55rem; border-radius: 4px; font-weight: bold; }
        .console { background: #000; border: 1px solid #581c87; padding: 12px; height: 280px; overflow-y: auto; font-size: 0.65rem; color: #e9d5ff; border-radius: 6px; line-height: 1.4; }
        .console div { margin-bottom: 3px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <div class="title">QLUX ABSOLUTE NODE</div>
            <div class="subtitle">// 純粋な価値の流通だけを残し、美しく調和する次世代ノード</div>
            <div class="feed-bar">✨ NODE STATUS: ABSOLUTE SYNC ACTIVE [100% OPERATIONAL]</div>
        </div>

        <div class="grid">
            <div class="card"><div class="card-title">NODE TPS</div><div class="card-val" id="val-tps" style="color: #38bdf8;">888,888,888,000</div></div>
            <div class="card"><div class="card-title">LATENCY</div><div class="card-val" id="val-latency" style="color: #34d399;">0.0000 ms</div></div>
            <div class="card"><div class="card-title">NODE TIER</div><div class="card-val" id="val-tier" style="color: #fbbf24;">ABSOLUTE-01</div></div>
            <div class="card"><div class="card-title">WEALTH FOUNTAIN</div><div class="card-val" id="val-wealth" style="color: #f472b6;">∞ SATOSHIS</div></div>
        </div>

        <!-- GLOBAL SYNCHRONIZATION MODULE BUTTONS (CLICKABLE) -->
        <div class="sync-section">
            <div class="sync-title">GLOBAL SYNCHRONIZATION</div>
            <div class="sync-sub">地球規模の同調性を担保するモジュール群（タップして各中枢へ遷移）</div>
            <div class="sync-grid">
                <a href="/module/qluxwallet" class="sync-btn">01 // qluxwallet</a>
                <a href="/module/qluxprime" class="sync-btn">03 // QLUXPRIME</a>
                <a href="/module/flow" class="sync-btn">04 // FLOW</a>
                <a href="/module/axiom" class="sync-btn">05 // AXIOM</a>
                <a href="/module/logic" class="sync-btn">06 // LOGIC</a>
                <a href="/module/prime" class="sync-btn">07 // PRIME</a>
                <a href="/module/omega" class="sync-btn active-omega">08 // OMEGA</a>
                <a href="/module/void" class="sync-btn">09 // VOID</a>
                <a href="/module/zen" class="sync-btn">10 // ZEN</a>
                <a href="/module/true" class="sync-btn">11 // TRUE</a>
                <a href="/module/core" class="sync-btn">12 // CORE</a>
            </div>
        </div>

        <div class="console-container">
            <div class="console-header">
                <span>ABSOLUTE NODE TELEMETRY STREAM</span>
                <span class="badge">ONLINE</span>
            </div>
            <div class="console" id="console-log">
                <div>[AbsoluteNode] Initializing QLUX ABSOLUTE NODE core telemetry...</div>
            </div>
        </div>
    </div>
    <script>
        const consoleEl = document.getElementById('console-log');
        const logs = [
            "[AbsoluteNode] Core online and synchronized with global mesh.",
            "[Telemetry] Quantum hash validation stream stable."
        ];

        async function triggerNodeCycle() {
            try {
                const payload = Array.from({length: 500}, (_, i) => `NODE_PACKET_${Math.random()}`);
                const response = await fetch('/api/node/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stream: payload })
                });
                const result = await response.json();
                
                document.getElementById('val-tps').innerText = result.tps.toLocaleString() + " TPS";
                document.getElementById('val-latency').innerText = result.latency_ms.toFixed(4) + " ms";
                document.getElementById('val-wealth').innerText = result.wealth_accumulator.toLocaleString() + " SATs";

                const now = new Date();
                const timeStr = now.toTimeString().split(' ')[0] + "." + String(now.getMilliseconds()).padStart(3, '0');
                
                logs.push(`[${timeStr}] NODE_SYNC_BURST | RootHash: ${result.root_hash.substring(0, 20)}... | Status: OK`);
                if (logs.length > 40) logs.shift();

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

@app.route('/module/<name>')
def module_redirect(name):
    # 各モジュールボタンを押したときに表示される専用ページ
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MODULE // {name.upper()}</title>
        <style>
            body {{ background: #000; color: #a855f7; font-family: 'Courier New', monospace; padding: 20px; text-align: center; box-sizing: border-box; }}
            .box {{ border: 2px solid #a855f7; padding: 30px 20px; border-radius: 10px; max-width: 600px; margin: 40px auto; background: #0d061c; box-shadow: 0 0 50px rgba(168,85,247,0.4); }}
            h1 {{ color: #c084fc; letter-spacing: 2px; font-size: 1.4rem; }}
            p {{ color: #cbd5e1; font-size: 0.85rem; line-height: 1.6; }}
            a {{ display: inline-block; margin-top: 25px; color: #fff; background: #7e22ce; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.8rem; box-shadow: 0 0 15px rgba(168,85,247,0.5); }}
            a:hover {{ background: #9333ea; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>MODULE: {name.upper()}</h1>
            <p>量子同期プロトコルが正常に確立されました。<br>分散中枢モジュール「{name.upper()}」は現在稼働中であり、因果律の統合処理を実行しています。</p>
            <a href="/">← ABSOLUTE NODE へ戻る</a>
        </div>
    </body>
    </html>
    """)

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

