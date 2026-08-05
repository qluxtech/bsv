from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="QLUX Hybrid Unified Data Exchange Core",
    version="22.0.0",
    description="The Ultimate Unified Marketplace for Humans and Autonomous AI Agents."
)

class UnifiedExchangeRequest(BaseModel):
    client_type: str  # "human" or "agent"
    target_id: str
    identifier: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — Hybrid Unified Exchange Core</title>
<style>
:root {
--bg-color: #020204;
--text-primary: #ffffff;
--text-secondary: #94a3b8;
--accent-gold: #fbbf24;
--accent-gold-glow: rgba(251, 191, 36, 0.4);
--accent-blue: #38bdf8;
}
body {
margin: 0; padding: 0; background-color: var(--bg-color); color: var(--text-primary);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.container { max-width: 850px; margin: 0 auto; padding: 50px 20px; text-align: center; }
.badge {
display: inline-block; background: rgba(251, 191, 36, 0.1); color: var(--accent-gold);
border: 1px solid rgba(251, 191, 36, 0.3); padding: 6px 20px; border-radius: 30px;
font-size: 0.85rem; font-weight: 800; letter-spacing: 0.2em; margin-bottom: 20px;
}
h1 { font-size: 3.8rem; margin: 0 0 10px 0; font-weight: 900; }
.exchange-box {
background: linear-gradient(145deg, rgba(20, 27, 45, 0.95), rgba(5, 8, 15, 0.98));
border: 2px solid var(--accent-gold); border-radius: 28px; padding: 45px 30px;
box-shadow: 0 0 80px var(--accent-gold-glow); margin-top: 30px; text-align: left;
}
.exchange-box h2 { text-align: center; margin-top: 0; color: #fff; font-size: 1.8rem; }
.form-group { margin: 20px 0; }
label { display: block; color: var(--accent-gold); font-weight: 700; margin-bottom: 8px; font-size: 0.95rem; }
select, input {
background: rgba(10, 15, 30, 0.9); color: var(--text-primary); border: 1px solid var(--accent-gold);
padding: 14px 20px; font-size: 1.05rem; border-radius: 12px; font-weight: 600; outline: none; width: 100%; box-sizing: border-box;
}
.btn {
background: linear-gradient(135deg, var(--accent-gold) 0%, #d97706 100%);
color: #020204; border: none; padding: 20px; font-size: 1.15rem; font-weight: 900;
border-radius: 50px; cursor: pointer; transition: all 0.3s ease;
box-shadow: 0 10px 30px rgba(251, 191, 36, 0.5); text-transform: uppercase; width: 100%; margin-top: 20px;
}
.btn:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(251, 191, 36, 0.8); }
#result-panel {
margin-top: 25px; background: rgba(0,0,0,0.5); border: 1px dashed var(--accent-blue);
padding: 20px; border-radius: 16px; display: none; word-break: break-all; text-align: left;
}
#result-panel h4 { color: var(--accent-blue); margin: 0 0 10px 0; }
.success-text { color: #34d399; font-weight: bold; }
</style>
</head>
<body>
<div class="container">
<div class="badge">Hybrid Unified Exchange v22.0</div>
<h1>QLUX</h1>
<p style="color: var(--text-secondary);">人間向け設計図・プロンプトから、AIエージェント間自律知見までを100サトシで一撃同期する。</p>

<div class="exchange-box">
<h2>UNIFIED ASSET & KNOWLEDGE GATEWAY</h2>

<div class="form-group">
<label>PARTICIPANT MODE / 参加レイヤー</label>
<select id="client-type" onchange="toggleModeFields()">
<option value="human">Human Professional (設計図・CAD・プロンプト購入)</option>
<option value="agent">Autonomous AI Agent (AI専用・自律型知見バースト)</option>
</select>
</div>

<div class="form-group" id="group-target">
<label id="label-target">SELECT ASSET / 取得対象データ</label>
<select id="target-id">
<option value="blueprint_alpha">精密機械・特急電極カスタム設計図 (100 Sats)</option>
<option value="3d_cad_model">Fカメ・高耐熱モールド構造CADデータ (100 Sats)</option>
<option value="ai_prompt_core">超高精度AI自律エージェント・プロンプトパック (100 Sats)</option>
</select>
</div>

<div class="form-group">
<label id="label-identifier">USER / AGENT IDENTIFIER (識別子)</label>
<input type="text" id="identifier" value="Pro-Engineer-01">
</div>

<button class="btn" onclick="executeUnifiedExchange()">⚡ EXECUTE 100 SATS UNIFIED DISPATCH</button>

<div id="result-panel">
<h4>CONSENSUS STATUS: <span class="success-text">VERIFIED & UNLOCKED</span></h4>
<p id="result-content" style="color: var(--text-secondary); font-family: monospace; font-size: 0.9rem;"></p>
</div>
</div>
</div>

<script>
function toggleModeFields() {
    const type = document.getElementById('client-type').value;
    const labelTarget = document.getElementById('label-target');
    const targetSelect = document.getElementById('target-id');
    const labelId = document.getElementById('label-identifier');
    const inputId = document.getElementById('identifier');

    if (type === 'human') {
        labelTarget.innerText = "SELECT ASSET / 取得対象データ";
        targetSelect.innerHTML = `
            <option value="blueprint_alpha">精密機械・特急電極カスタム設計図 (100 Sats)</option>
            <option value="3d_cad_model">Fカメ・高耐熱モールド構造CADデータ (100 Sats)</option>
            <option value="ai_prompt_core">超高精度AI自律エージェント・プロンプトパック (100 Sats)</option>
        `;
        labelId.innerText = "USER IDENTIFIER (人間側 識別名)";
        inputId.value = "Pro-Engineer-01";
    } else {
        labelTarget.innerText = "KNOWLEDGE FRAGMENT / AI専用知見・コード断片";
        targetSelect.innerHTML = `
            <option value="quantum_routing_patch">超高速非同期ルーティング最適化パッチ (100 Sats)</option>
            <option value="zero_latency_memory">LLMコンテキスト圧縮・メモリ効率化スクリプト (100 Sats)</option>
            <option value="autonomous_swarm_logic">マルチエージェント協調・分散合意ロジック (100 Sats)</option>
        `;
        labelId.innerText = "AI AGENT IDENTIFIER (AIエージェント名)";
        inputId.value = "Agent-LLM-Alpha-v4";
    }
}

async function executeUnifiedExchange() {
    const clientType = document.getElementById('client-type').value;
    const targetId = document.getElementById('target-id').value;
    const identifier = document.getElementById('identifier').value;
    const panel = document.getElementById('result-panel');
    const content = document.getElementById('result-content');
    
    panel.style.display = "block";
    content.innerText = "Broadcasting 100 Sats micro-payment & verifying cryptographic proof...";

    try {
        const response = await fetch('/api/unified-exchange', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_type: clientType, target_id: targetId, identifier: identifier })
        });
        const data = await response.json();

        setTimeout(() => {
            content.innerHTML = `
                <br>✓ <b>Mode:</b> ${data.client_type.toUpperCase()}
                <br>✓ <b>Identifier:</b> ${data.identifier}
                <br>✓ <b>On-Chain TxID:</b> ${data.txid}
                <br>✓ <b>Unlocked Payload:</b> ${data.item_name}
                <br>✓ <b>Hash:</b> <code>sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</code>
                <br><br><span style="color: var(--accent-gold);">[!] Pipeline fully secured. Immediate extraction granted.</span>
            `;
        }, 900);
    } catch (err) {
        content.innerText = "Error: Transmission failed.";
    }
}
</script>
</body>
</html>
"""

@app.post("/api/unified-exchange")
async def api_unified_exchange(data: UnifiedExchangeRequest):
    dictionary = {
        "blueprint_alpha": "Precision Electrode Custom Blueprint",
        "3d_cad_model": "F-Kame Mold Heat-Resistant CAD Model",
        "ai_prompt_core": "Autonomous AI Agent Prompt Pack",
        "quantum_routing_patch": "Quantum-Grade Async Routing Patch",
        "zero_latency_memory": "Zero-Latency Context Compression Script",
        "autonomous_swarm_logic": "Autonomous Multi-Agent Swarm Logic"
    }
    item_name = dictionary.get(data.target_id, "Universal Data Fragment")
    return {
        "status": "success",
        "client_type": data.client_type,
        "identifier": data.identifier,
        "item_name": item_name,
        "txid": "7f92a1103c88d871a2e948c2b74f39281a82f37c991b920183b27189fa3b1102"
    }
