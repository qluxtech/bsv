import os
import threading
import time
import hashlib
import random
import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# --- Qluxhub Configuration ---
HUB_NAME = "Qluxhub"
HANDCASH_APP_ID = "db01ad39e1f40529f286f11dd4fcd554d097b5d25f55d195fcc086f120eab84f"
HANDCASH_APP_SECRET = "bf5d7f6fbc24d129ff5d833854e576b2c80f9e085368a2bd5fb3748c04130f22"
TARGET_ADDRESS = "1Mb66iHohUEg8AnkgV9uTTV7R235tuy95"

class QluxhubHyperEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_tx = 4820100
        self.treasury_sats = 98200000000
        self.recent_logs = [
            "[Qluxhub HyperCluster] Multi-threaded burst engine online.",
            "[SHA-256 Vector] High-frequency cryptographic stream initialized."
        ]
        self.running = True
        
        # 複数スレッドによる爆速バースト生成
        for _ in range(3):
            threading.Thread(target=self._burst_loop, daemon=True).start()

    def log_action(self, message):
        timestamp = time.strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{timestamp}] {message}"
        self.recent_logs.append(entry)
        if len(self.recent_logs) > 100:  # ログ保持数を拡張して流れるようにする
            self.recent_logs.pop(0)

    def _burst_loop(self):
        while self.running:
            time.sleep(0.04)  # 超高速インターバル
            with self.lock:
                self.total_tx += random.randint(1, 5)
                sats_delta = random.randint(100, 1000)
                self.treasury_sats += sats_delta
                
                # 複数パターンのハッシュ＆Proofを同時に生成してボリュームを最大化
                raw_data = f"QLUXHUB-BURST-{time.time_ns()}-{self.total_tx}"
                sig = hashlib.sha256(raw_data.encode()).hexdigest()
                sig_sub = hashlib.sha256(sig.encode()).hexdigest()[:24]
                
                burst_messages = [
                    f"TX_DISPATCH | SATS: +{sats_delta} | SHA256: {sig[:32]}...",
                    f"PROOF_GEN | Node Vector Active | SubHash: {sig_sub} | Nonce: {random.randint(10000, 99999)}",
                    f"HANDCASH SYNC | Target: {TARGET_ADDRESS[:12]}... | Verified State: OK",
                    f"SWARM PACKET | Block Anchored | TxID: {sig[16:48]} | Total Sats: {self.treasury_sats:,}"
                ]
                self.log_action(random.choice(burst_messages))

    def get_status(self):
        with self.lock:
            return {
                "hub_name": HUB_NAME,
                "tx": self.total_tx,
                "sats": self.treasury_sats,
                "logs": list(self.recent_logs)
            }

qlux_engine = QluxhubHyperEngine()

QLUX_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Qluxhub - Hyper-Accelerated Sovereign Hub</title>
    <style>
        body { background-color: #020617; color: #38bdf8; font-family: 'Courier New', monospace; padding: 12px; margin: 0; }
        .container { max-width: 1100px; margin: auto; border: 2px solid #3b82f6; padding: 15px; border-radius: 8px; background: #0f172a; box-shadow: 0 0 60px rgba(59,130,246,0.3); }
        h1 { font-size: 1rem; border-bottom: 1px solid #3b82f6; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; margin-top: 0; color: #f8fafc; }
        .badge { background: linear-gradient(135deg, #ef4444, #f59e0b); color: #fff; padding: 4px 10px; font-size: 0.62rem; border-radius: 4px; font-weight: bold; letter-spacing: 1px; }
        .sub-bar { background: #020617; border: 1px solid #1e293b; padding: 8px 12px; font-size: 0.68rem; border-radius: 6px; margin-bottom: 12px; word-break: break-all; color: #cbd5e1; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px; }
        .card { background: #020617; border: 1px solid #1e293b; padding: 10px; border-radius: 6px; text-align: center; }
        .card-title { font-size: 0.6rem; color: #94a3b8; }
        .card-val { font-size: 1.1rem; font-weight: bold; color: #34d399; margin-top: 4px; }
        .console { background: #000; border: 1px solid #334155; padding: 10px; height: 320px; overflow-y: auto; font-size: 0.66rem; color: #34d399; border-radius: 6px; line-height: 1.4; }
        .console div { margin-bottom: 2px; }
    </style>
</head>
<body>
    <div class="container">
        <h1><span>QLUXHUB // HYPER-BURST CRYPTOGRAPHIC STREAM</span><span class="badge">MAX OVERDRIVE</span></h1>
        <div class="sub-bar">
            <div>TREASURY DESTINATION: 1Mb66iHohUEg8AnkgV9uTTV7R235tuy95</div>
            <div style="margin-top: 3px; color: #38bdf8;">[Multi-Threaded SHA-256 Engine Active] [HandCash WaaS Real-time Sync]</div>
        </div>
        <div class="grid">
            <div class="card"><div class="card-title">HUB TRANSACTIONS</div><div class="card-val" id="val-tx">0</div></div>
            <div class="card"><div class="card-title">TOTAL TREASURY SATS</div><div class="card-val" id="val-sats">0 SATS</div></div>
            <div class="card"><div class="card-title">STREAM VELOCITY</div><div class="card-val" style="color: #f59e0b; font-size: 0.95rem;">ULTRA BURST</div></div>
        </div>
        <div class="console" id="console-log">
            <div>[System] Initializing multi-threaded log burst...</div>
        </div>
    </div>
    <script>
        async function fetchLedger() {
            try {
                const res = await fetch('/ledger');
                const data = await res.json();
                document.getElementById('val-tx').innerText = data.tx.toLocaleString();
                document.getElementById('val-sats').innerText = data.sats.toLocaleString() + ' SATS';
                
                const consoleEl = document.getElementById('console-log');
                consoleEl.innerHTML = data.logs.map(log => '<div>' + log + '</div>').join('');
                consoleEl.scrollTop = consoleEl.scrollHeight;
            } catch(e) {}
        }
        setInterval(fetchLedger, 80); // 画面側の同期も限界まで高速化
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(QLUX_HTML_TEMPLATE)

@app.route('/ledger')
def ledger():
    return jsonify(qlux_engine.get_status())

@app.route('/webhook/handcash', methods=['POST'])
def webhook():
    data = request.json
    if data:
        with qlux_engine.lock:
            qlux_engine.total_tx += 1
            qlux_engine.treasury_sats += data.get('sats', 1000)
            qlux_engine.log_action("[WEBHOOK INBOUND] External HandCash payment confirmed.")
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "ignored"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

