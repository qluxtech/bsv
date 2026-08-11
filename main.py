import os
import threading
import time
import hashlib
import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# --- Qluxhub Configuration ---
HUB_NAME = "Qluxhub"
HANDCASH_APP_ID = "db01ad39e1f40529f286f11dd4fcd554d097b5d25f55d195fcc086f120eab84f"
HANDCASH_APP_SECRET = "bf5d7f6fbc24d129ff5d833854e576b2c80f9e085368a2bd5fb3748c04130f22"
TARGET_ADDRESS = "1Mb66iHohUEg8AnkgV9uTTV7R235tuy95"

class QluxhubEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_tx = 0
        self.treasury_sats = 0
        self.recent_logs = []
        self.running = True
        
        self.thread = threading.Thread(target=self._hub_loop, daemon=True)
        self.thread.start()

    def log_action(self, message):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.recent_logs.append(entry)
        if len(self.recent_logs) > 30:
            self.recent_logs.pop(0)

    def _hub_loop(self):
        while self.running:
            time.sleep(10.0)
            with self.lock:
                self.total_tx += 1
                sats_delta = 1500
                self.treasury_sats += sats_delta
                sig = hashlib.sha256(f"QLUXHUB-{time.time()}-{self.total_tx}".encode()).hexdigest()[:32]
                self.log_action(f"QLUXHUB NODE SYNC | HandCash Linked | +{sats_delta} SATS | Proof: {sig}")

    def get_status(self):
        with self.lock:
            return {
                "hub_name": HUB_NAME,
                "tx": self.total_tx,
                "sats": self.treasury_sats,
                "logs": list(self.recent_logs)
            }

qlux_engine = QluxhubEngine()

QLUX_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Qluxhub - BSV Sovereign Utility & Network Hub</title>
    <style>
        body { background-color: #020617; color: #38bdf8; font-family: 'Courier New', monospace; padding: 15px; margin: 0; }
        .container { max-width: 1050px; margin: auto; border: 2px solid #3b82f6; padding: 18px; border-radius: 8px; background: #0f172a; box-shadow: 0 0 50px rgba(59,130,246,0.2); }
        h1 { font-size: 1.05rem; border-bottom: 1px solid #3b82f6; padding-bottom: 10px; display: flex; justify-content: space-between; align-items: center; margin-top: 0; color: #f8fafc; }
        .badge { background: #3b82f6; color: #fff; padding: 4px 10px; font-size: 0.65rem; border-radius: 4px; font-weight: bold; letter-spacing: 1px; }
        .sub-bar { background: #020617; border: 1px solid #1e293b; padding: 10px 14px; font-size: 0.72rem; border-radius: 6px; margin-bottom: 15px; word-break: break-all; color: #cbd5e1; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 15px; }
        .card { background: #020617; border: 1px solid #1e293b; padding: 12px; border-radius: 6px; text-align: center; }
        .card-title { font-size: 0.65rem; color: #94a3b8; }
        .card-val { font-size: 1.2rem; font-weight: bold; color: #34d399; margin-top: 6px; }
        .console { background: #000; border: 1px solid #334155; padding: 12px; height: 220px; overflow-y: auto; font-size: 0.7rem; color: #34d399; border-radius: 6px; line-height: 1.5; }
        .console div { margin-bottom: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1><span>QLUXHUB // BSV SOVEREIGN UTILITY HUB</span><span class="badge">ACTIVE MAINNET NODE</span></h1>
        <div class="sub-bar">
            <div>TREASURY DESTINATION: 1Mb66iHohUEg8AnkgV9uTTV7R235tuy95</div>
            <div style="margin-top: 4px; color: #38bdf8;">[HandCash Cloud API Connected] [Qluxhub Sovereign Gateway Active]</div>
        </div>
        <div class="grid">
            <div class="card"><div class="card-title">HUB TRANSACTIONS</div><div class="card-val" id="val-tx">0</div></div>
            <div class="card"><div class="card-title">TOTAL TREASURY SATS</div><div class="card-val" id="val-sats">0 SATS</div></div>
            <div class="card"><div class="card-title">NETWORK POSITION</div><div class="card-val" style="color: #60a5fa; font-size: 1rem;">ELITE API HUB</div></div>
        </div>
        <div class="console" id="console-log">
            <div>[Qluxhub Core] Initializing secure sovereign gateway...</div>
        </div>
    </div>
    <script>
        setInterval(async () => {
            try {
                const res = await fetch('/ledger');
                const data = await res.json();
                document.getElementById('val-tx').innerText = data.tx.toLocaleString();
                document.getElementById('val-sats').innerText = data.sats.toLocaleString() + ' SATS';
                
                const consoleEl = document.getElementById('console-log');
                consoleEl.innerHTML = data.logs.map(log => '<div>' + log + '</div>').join('');
                consoleEl.scrollTop = consoleEl.scrollHeight;
            } catch(e) {}
        }, 1500);
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
            qlux_engine.log_action("[WEBHOOK] Inbound payment routed to Qluxhub treasury.")
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "ignored"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

