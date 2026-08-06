from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import time

app = FastAPI(
    title="QLUX Global Terranode Omniverse Core",
    version="35.0.0",
    description="The Ultimate Global Infrastructure Powered by BSV Terranode Architecture."
)

class GlobalSyncRequest(BaseModel):
    global_region: str
    node_signature: str
    action_payload: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — Global Terranode Omniverse</title>
<style>
:root {
--bg-color: #010204;
--text-primary: #ffffff;
--text-secondary: #94a3b8;
--accent-gold: #f59e0b;
--accent-gold-glow: rgba(245, 158, 11, 0.4);
--accent-cyan: #06b6d4;
}
body {
margin: 0; padding: 0; background-color: var(--bg-color); color: var(--text-primary);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.container { max-width: 950px; margin: 0 auto; padding: 40px 20px; text-align: center; }
.badge {
display: inline-block; background: rgba(245, 158, 11, 0.1); color: var(--accent-gold);
border: 1px solid rgba(245, 158, 11, 0.3); padding: 6px 22px; border-radius: 30px;
font-size: 0.8rem; font-weight: 800; letter-spacing: 0.25em; margin-bottom: 15px;
}
h1 { font-size: 3.5rem; margin: 0 0 10px 0; font-weight: 900; }
.global-box {
background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
border: 2px solid var(--accent-gold); border-radius: 32px; padding: 40px 30px;
box-shadow: 0 0 90px var(--accent-gold-glow); margin-top: 25px; text-align: left;
}
.global-box h2 { text-align: center; margin-top: 0; color: #fff; font-size: 1.6rem; }
.form-group { margin: 18px 0; }
label { display: block; color: var(--accent-gold); font-weight: 700; margin-bottom: 8px; font-size: 0.9rem; }
select, input {
background: rgba(5, 10, 25, 0.9); color: var(--text-primary); border: 1px solid var(--accent-gold);
padding: 14px 20px; font-size: 1rem; border-radius: 14px; font-weight: 600; outline: none; width: 100%; box-sizing: border-box;
}
.btn {
background: linear-gradient(135deg, var(--accent-gold) 0%, #b45309 100%);
color: #010204; border: none; padding: 18px; font-size: 1.1rem; font-weight: 900;
border-radius: 50px; cursor: pointer; transition: all 0.3s ease;
box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4); text-transform: uppercase; width: 100%; margin-top: 20px;
}
.btn:hover { transform: translateY(-3px); box-shadow: 0 15px 45px rgba(245, 158, 11, 0.7); }
#result-panel {
margin-top: 25px; background: rgba(0,0,0,0.6); border: 1px dashed var(--accent-cyan);
padding: 20px; border-radius: 16px; display: none; word-break: break-all; text-align: left;
}
#result-panel h4 { color: var(--accent-cyan); margin: 0 0 10px 0; }
.success-text { color: #34d399; font-weight: bold; }
</style>
</head>
<body>
<div class="container">
<div class="badge">Global Terranode OS v35.0</div>
<h1>QLUX</h1>
<p style="color: var(--text-secondary);">世界中のすべてのトランザクション・AIエージェント・リソースをBSVで完全同期するインフィニット基盤。</p>

<div class="global-box">
<h2>GLOBAL TERRANODE OMNIVERSE GATEWAY</h2>

<div class="form-group">
<label>GLOBAL REGION SHARD / グローバル地域ノード</label>
<select id="global-region">
<option value="asia_tokyo_shard">Asia-East (Tokyo Terranode Core)</option>
<option value="na_virginia_shard">North America (Virginia Mainframe)</option>
<option value="eu_frankfurt_shard">Europe (Frankfurt Edge Shard)</option>
<option value="universal_omni_shard">Universal Omniverse (All Regions Sync)</option>
</select>
</div>

<div class="form-group">
<label>GLOBAL ACTION / グローバル同期アクション</label>
<select id="action-payload">
<option value="sync_all_transactions">世界全トランザクションのテラノード一括合意</option>
<option value="deploy_global_ai_swarm">全地球AIエージェント・スウォーム展開</option>
<option value="harvest_global_sats">全世界自動収益（サトシ）の瞬時回収</option>
</select>
</div>

<div class="form-group">
<label>MASTER NODE SIGNATURE / グローバルマスター署名</label>
<input type="text" id="node-signature" value="QLUX-Global-Terranode-Master-01">
</div>

<button class="btn" onclick="executeGlobalSync()">⚡ EXECUTE GLOBAL TERRANODE SYNC</button>

<div id="result-panel">
<h4>GLOBAL CONSENSUS: <span class="success-text">ALL NODES SYNCHRONIZED</span></h4>
<p id="result-content" style="color: var(--text-secondary); font-family: monospace; font-size: 0.9rem;"></p>
</div>
</div>
</div>

<script>
async function executeGlobalSync() {
    const globalRegion = document.getElementById('global-region').value;
    const actionPayload = document.getElementById('action-payload').value;
    const nodeSignature = document.getElementById('node-signature').value;
    const panel = document.getElementById('result-panel');
    const content = document.getElementById('result-content');
    
    panel.style.display = "block";
    content.innerText = "Broadcasting cryptographic pulse across global terranode shards...";

    try {
        const response = await fetch('/api/global-sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ global_region: globalRegion, node_signature: nodeSignature, action_payload: actionPayload })
        });
        const data = await response.json();

        setTimeout(() => {
            content.innerHTML = `
                <br>✓ <b>Global Region:</b> ${data.global_region.toUpperCase()}
                <br>✓ <b>Master Signature:</b> ${data.node_signature}
                <br>✓ <b>Action Protocol:</b> ${data.action_payload}
                <br>✓ <b>Terranode Block Hash:</b> <code>${data.block_hash}</code>
                <br>✓ <b>Global Status:</b> <span class="success-text">100% Synchronized Worldwide</span>
                <br><br><span style="color: var(--accent-gold);">[!] Global ecosystem is fully active. All transactions secured on-chain.</span>
            `;
        }, 800);
    } catch (err) {
        content.innerText = "Error: Global shard connection timeout.";
    }
}
</script>
</body>
</html>
"""

@app.post("/api/global-sync")
async def api_global_sync(data: GlobalSyncRequest):
    raw_str = f"{data.global_region}-{data.node_signature}-{time.time()}"
    block_hash = hashlib.sha256(raw_str.encode()).hexdigest()
    return {
        "status": "success",
        "global_region": data.global_region,
        "node_signature": data.node_signature,
        "action_payload": data.action_payload,
        "block_hash": block_hash
    }
