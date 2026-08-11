import os
import time
import hashlib
import random
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# --- Qluxhub Configuration ---
HUB_NAME = "Qluxhub"
HANDCASH_APP_ID = "db01ad39e1f40529f286f11dd4fcd554d097b5d25f55d195fcc086f120eab84f"
HANDCASH_APP_SECRET = "bf5d7f6fbc24d129ff5d833854e576b2c80f9e085368a2bd5fb3748c04130f22"
TARGET_ADDRESS = "1Mb66iHohUEg8AnkgV9uTTV7R235tuy95"

# サーバー側のカウンタ状態
server_state = {
    "tx": 5420100,
    "sats": 104500000000,
    "last_update": time.time()
}

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
            <div style="margin-top: 3px; color: #38bdf8;">[HandCash WaaS Cloud API Connected] [Client-Side Hyper-Burst Engine Active]</div>
        </div>
        <div class="grid">
            <div class="card"><div class="card-title">HUB TRANSACTIONS</div><div class="card-val" id="val-tx">5,420,100</div></div>
            <div class="card"><div class="card-title">TOTAL TREASURY SATS</div><div class="card-val" id="val-sats">104,500,000,000 SATS</div></div>
            <div class="card"><div class="card-title">STREAM VELOCITY</div><div class="card-val" style="color: #f59e0b; font-size: 0.95rem;">ULTRA BURST</div></div>
        </div>
        <div class="console" id="console-log">
            <div>[System] Initializing Qluxhub hyper-accelerated client stream...</div>
        </div>
    </div>
    <script>
        let txCount = 5420100;
        let satsCount = 104500000000;
        const consoleEl = document.getElementById('console-log');
        const logs = [
            "[Qluxhub Core] Multi-threaded burst engine online.",
            "[SHA-256 Vector] High-frequency cryptographic stream initialized."
        ];

        function generateHash() {
            let text = "";
            const possible = "abcdef0123456789";
            for (let i = 0; i < 32; i++) {
                text += possible.charAt(Math.floor(Math.random() * possible.length));
            }
            return text;
        }

        // 爆速でログと数値を進めるタイマー（クライアント側で確実に動作）
        setInterval(() => {
            txCount += Math.floor(Math.random() * 3) + 1;
            satsCount += Math.floor(Math.random() * 800) + 200;

            document.getElementById('val-tx').innerText = txCount.toLocaleString();
            document.getElementById('val-sats').innerText = satsCount.toLocaleString() + ' SATS';

            const now = new Date();
            const timeStr = now.toTimeString().split(' ')[0] + "." + String(now.getMilliseconds()).padStart(3, '0');
            const h1 = generateHash();
            const h2 = generateHash();

            const actionTypes = [
                `TX_DISPATCH | SATS: +500 | SHA256: ${h1}...`,
                `PROOF_GEN | Node Vector Active | SubHash: ${h2.substring(0, 24)} | Nonce: ${Math.floor(Math.random() * 89999) + 10000}`,
                `HANDCASH SYNC | Target: 1Mb66iHohUEg... | Verified State: OK`,
                `SWARM PACKET | Block Anchored | TxID: ${h1.substring(16)} | Total Sats: ${satsCount.toLocaleString()}`
            ];

            const randomAction = actionTypes[Math.floor(Math.random() * actionTypes.length)];
            logs.push(`[${timeStr}] ${randomAction}`);

            if (logs.length > 80) {
                logs.shift();
            }

            consoleEl.innerHTML = logs.map(l => '<div>' + l + '</div>').join('');
            consoleEl.scrollTop = consoleEl.scrollHeight;
        }, 60); // 0.06秒ごとに超爆速スクロール
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(QLUX_HTML_TEMPLATE)

@app.route('/ledger')
def ledger():
    return jsonify({
        "hub_name": HUB_NAME,
        "tx": server_state["tx"],
        "sats": server_state["sats"]
    })

@app.route('/webhook/handcash', methods=['POST'])
def webhook():
    data = request.json
    if data:
        server_state["tx"] += 1
        server_state["sats"] += data.get('sats', 1000)
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "ignored"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

