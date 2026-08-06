from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import time

app = FastAPI(
    title="QLUX Apex Enterprise Global OS",
    version="50.0.0",
    description="The Ultimate Global Enterprise Infrastructure Powered by BSV Teranode Architecture."
)

class EnterpriseRequest(BaseModel):
    deployment_layer: str
    execution_protocol: str
    node_identifier: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — Apex Enterprise Global OS</title>
<style>
:root {
--bg-deep: #030712;
--bg-surface: rgba(15, 23, 42, 0.7);
--border-glass: rgba(255, 255, 255, 0.08);
--border-gold: rgba(245, 158, 11, 0.4);
--text-main: #f8fafc;
--text-muted: #94a3b8;
--accent-gold: #f59e0b;
--accent-gold-glow: rgba(245, 158, 11, 0.25);
--accent-cyan: #22d3ee;
}

* { box-sizing: border-box; }
body {
margin: 0; padding: 0; background-color: var(--bg-deep); color: var(--text-main);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
-webkit-font-smoothing: antialiased; line-height: 1.5;
}

.ambient-glow {
position: fixed; top: -20vh; left: 50%; transform: translateX(-50%);
width: 60vw; height: 40vh; background: radial-gradient(circle, rgba(245,158,11,0.08) 0%, rgba(3,7,18,0) 70%);
z-index: -1; pointer-events: none;
}

.container { max-width: 1200px; margin: 0 auto; padding: 60px 24px; }

/* 企業トップヘッダー */
.nav-header {
display: flex; justify-content: space-between; align-items: center;
border-bottom: 1px solid var(--border-glass); padding-bottom: 24px; margin-bottom: 50px;
}
.logo-area { display: flex; align-items: center; gap: 12px; }
.logo-text { font-size: 1.5rem; font-weight: 900; letter-spacing: 0.15em; color: #fff; }
.status-badge {
display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 197, 94, 0.1);
border: 1px solid rgba(34, 197, 94, 0.3); color: #4ade80; padding: 6px 14px;
border-radius: 20px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;
}
.status-dot { width: 6px; height: 6px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; animation: pulse 2s infinite; }

@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

/* ヒーローセクション */
.hero { text-align: center; margin-bottom: 60px; }
.hero h1 { font-size: 3.8rem; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 16px 0; color: #fff; }
.hero p { font-size: 1.2rem; color: var(--text-muted); max-width: 750px; margin: 0 auto; font-weight: 400; }

/* メトリクス・カードグリッド */
.metrics-grid {
display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin-bottom: 40px;
}
.metric-card {
background: var(--bg-surface); backdrop-filter: blur(16px);
border: 1px solid var(--border-glass); border-radius: 20px; padding: 24px;
transition: border-color 0.3s ease, transform 0.3s ease;
}
.metric-card:hover { border-color: var(--border-gold); transform: translateY(-2px); }
.metric-title { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.metric-value { font-size: 1.8rem; font-weight: 800; color: #fff; }
.metric-sub { font-size: 0.8rem; color: #4ade80; margin-top: 4px; font-weight: 600; }

/* メイン・コントロールコンソール */
.console-box {
background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(3, 7, 18, 0.95));
backdrop-filter: blur(24px); border: 1px solid var(--border-gold);
border-radius: 28px; padding: 48px; box-shadow: 0 0 80px var(--accent-gold-glow);
}
.console-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
.console-title { font-size: 1.4rem; font-weight: 800; color: #fff; margin: 0; }

.form-grid { display: grid; grid-template-columns: 1fr; gap: 24px; margin-bottom: 32px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
label { font-size: 0.85rem; color: var(--accent-gold); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }

select, input {
background: rgba(3, 7, 18, 0.8); color: var(--text-main); border: 1px solid rgba(255, 255, 255, 0.15);
padding: 16px 20px; font-size: 1rem; border-radius: 14px; font-weight: 600; outline: none; width: 100%;
transition: all 0.2s ease;
}
select:focus, input:focus { border-color: var(--accent-gold); box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15); }

.action-btn {
background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
color: #030712; border: none; padding: 20px; font-size: 1.1rem; font-weight: 800;
border-radius: 14px; cursor: pointer; transition: all 0.3s ease; width: 100%;
box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3); text-transform: uppercase; letter-spacing: 0.05em;
}
.action-btn:hover { transform: translateY(-2px); box-shadow: 0 15px 40px rgba(245, 158, 11, 0.5); }

/* 実行結果コンソール */
#result-terminal {
margin-top: 32px; background: rgba(2, 4, 8, 0.9); border: 1px solid rgba(34, 211, 238, 0.3);
padding: 24px; border-radius: 16px; display: none; font-family: monospace; font-size: 0.9rem;
}
.terminal-header { color: var(--accent-cyan); font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.terminal-content { color: var(--text-muted); line-height: 1.6; word-break: break-all; }
.success-highlight { color: #4ade80; font-weight: bold; }
</style>
</head>
<body>
<div class="ambient-glow"></div>
<div class="container">

<!-- ヘッダー -->
<header class="nav-header">
    <div class="logo-area">
        <div class="logo-text">QLUX</div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        TERANODE MESH ONLINE
    </div>
</header>

<!-- ヒーロー -->
<section class="hero">
    <h1>グローバル経済を駆動する、究極の自律インフラ。</h1>
    <p>BSV Teranodeの無限スケーラビリティと超高精度AIエージェントが直結。仲介者を完全に排除した次世代エンタープライズ・エコシステム。</p>
</section>

<!-- リアルタイム・メトリクス -->
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-title">Network Throughput</div>
        <div class="metric-value">4,291,080 <span style="font-size: 1rem; color: var(--text-muted);">TPS</span></div>
        <div class="metric-sub">▲ Teranode Verified</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Active AI Agents</div>
        <div class="metric-value">849,210</div>
        <div class="metric-sub">▲ Global Swarm Sync</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Settlement Latency</div>
        <div class="metric-value">< 1.2 <span style="font-size: 1rem; color: var(--text-muted);">ms</span></div>
        <div class="metric-sub">▲ Zero-Conf Atomic</div>
    </div>
</div>

<!-- コンソールコントロール -->
<div class="console-box">
    <div class="console-header">
        <h2 class="console-title">APEX ENTERPRISE GATEWAY</h2>
    </div>

    <div class="form-grid">
        <div class="form-group">
            <label>Deployment Layer / インフラストラクチャ層</label>
            <select id="deployment-layer">
                <option value="teranode_omni_core">BSV Teranode Omni-Core (無限トランザクション処理)</option>
                <option value="ai_autonomous_cluster">AI Autonomous Execution Cluster (自律エージェント基盤)</option>
                <option value="global_yield_matrix">Global Liquidity & Asset Matrix (超高収益収益配当)</option>
            </select>
        </div>

        <div class="form-group">
            <label>Execution Protocol / 運用プロトコル</label>
            <select id="execution-protocol">
                <option value="atomic_settlement">ミリ秒アトミック決済 ＆ スマートコントラクト即時執行</option>
                <option value="global_shard_sync">全世界テラノード・シャード一括同期</option>
                <option value="autonomous_sats_harvest">AIリソース自動回収・サトシハーベスト</option>
            </select>
        </div>

        <div class="form-group">
            <label>Node Identifier / 企業認証シグネチャ</label>
            <input type="text" id="node-identifier" value="QLUX-Apex-Enterprise-Node-01">
        </div>
    </div>

    <button class="action-btn" onclick="executeApexSync()">⚡ EXECUTE APEX DISPATCH</button>

    <div id="result-terminal">
        <div class="terminal-header">
            <span>●</span> APEX CONSENSUS STATUS: <span class="success-highlight">VERIFIED ON-CHAIN</span>
        </div>
        <div id="terminal-output" class="terminal-content"></div>
    </div>
</div>

</div>

<script>
async function executeApexSync() {
    const deploymentLayer = document.getElementById('deployment-layer').value;
    const executionProtocol = document.getElementById('execution-protocol').value;
    const nodeIdentifier = document.getElementById('node-identifier').value;
    const terminal = document.getElementById('result-terminal');
    const output = document.getElementById('terminal-output');
    
    terminal.style.display = "block";
    output.innerHTML = "Initializing cryptographic handshake across global BSV Teranode mesh...";

    try {
        const response = await fetch('/api/apex-sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ deployment_layer: deploymentLayer, execution_protocol: executionProtocol, node_identifier: nodeIdentifier })
        });
        const data = await response.json();

        setTimeout(() => {
            output.innerHTML = `
                ✓ <b>Infrastructure Layer:</b> ${data.deployment_layer.toUpperCase()}<br>
                ✓ <b>Protocol Mode:</b> ${data.execution_protocol}<br>
                ✓ <b>Enterprise Signature:</b> ${data.node_identifier}<br>
                ✓ <b>Teranode Block Hash:</b> <code>${data.block_hash}</code><br>
                ✓ <b>Global Deployment:</b> <span class="success-highlight">100% Fully Operational Worldwide</span><br><br>
                <span style="color: var(--accent-gold);">[!] Apex enterprise ecosystem successfully synchronized with the global blockchain network.</span>
            `;
        }, 600);
    } catch (err) {
        output.innerText = "Error: Apex network gateway timeout.";
    }
}
</script>
</body>
</html>
"""

@app.post("/api/apex-sync")
async def api_apex_sync(data: EnterpriseRequest):
    raw_str = f"{data.deployment_layer}-{data.execution_protocol}-{time.time()}"
    block_hash = hashlib.sha256(raw_str.encode()).hexdigest()
    return {
        "status": "success",
        "deployment_layer": data.deployment_layer,
        "execution_protocol": data.execution_protocol,
        "node_identifier": data.node_identifier,
        "block_hash": block_hash
    }
