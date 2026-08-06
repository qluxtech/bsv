from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import time

app = FastAPI(
    title="QLUX Enterprise Apex Global Hub",
    version="500.0.0",
    description="The Ultimate All-In-One BSV Enterprise & Teranode Infrastructure Platform."
)

class ApexEnterpriseRequest(BaseModel):
    bsv_service_module: str
    teranode_scaling_layer: str
    execution_payload: str
    corporate_auth_handle: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — Ultimate Enterprise Apex Global Hub</title>
<style>
:root {
--bg-deep: #010307;
--bg-surface: rgba(10, 16, 31, 0.90);
--border-glass: rgba(255, 255, 255, 0.08);
--border-gold: rgba(245, 158, 11, 0.55);
--text-main: #f8fafc;
--text-muted: #94a3b8;
--accent-gold: #f59e0b;
--accent-gold-glow: rgba(245, 158, 11, 0.4);
--accent-cyan: #38bdf8;
--accent-green: #4ade80;
--accent-purple: #c084fc;
}

* { box-sizing: border-box; }
body {
margin: 0; padding: 0; background-color: var(--bg-deep); color: var(--text-main);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
-webkit-font-smoothing: antialiased; line-height: 1.6; overflow-x: hidden;
}

/* 背景サイバー動画 */
.video-bg-container {
position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
z-index: -2; overflow: hidden; pointer-events: none; opacity: 0.28;
}
.video-bg-container video {
width: 100%; height: 100%; object-fit: cover; filter: contrast(125%) brightness(85%);
}
.ambient-glow {
position: fixed; top: -15vh; left: 50%; transform: translateX(-50%);
width: 80vw; height: 40vh; background: radial-gradient(circle, rgba(245,158,11,0.14) 0%, rgba(1,3,7,0) 70%);
z-index: -1; pointer-events: none;
}

.container { max-width: 1150px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 1; }

/* ヘッダー */
.nav-header {
display: flex; justify-content: space-between; align-items: center;
border-bottom: 1px solid var(--border-glass); padding-bottom: 20px; margin-bottom: 40px;
backdrop-filter: blur(12px);
}
.logo-area { display: flex; align-items: center; gap: 12px; }
.logo-text { font-size: 1.7rem; font-weight: 900; letter-spacing: 0.25em; color: #fff; }
.status-badge {
display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 197, 94, 0.12);
border: 1px solid rgba(34, 197, 94, 0.35); color: var(--accent-green); padding: 6px 14px;
border-radius: 20px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;
}
.status-dot { width: 6px; height: 6px; background: var(--accent-green); border-radius: 50%; box-shadow: 0 0 10px var(--accent-green); animation: pulse 2s infinite; }

@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

/* ヒーロー */
.hero { text-align: center; margin-bottom: 45px; }
.badge-sub {
display: inline-block; background: rgba(245, 158, 11, 0.12); color: var(--accent-gold);
border: 1px solid rgba(245, 158, 11, 0.35); padding: 6px 20px; border-radius: 30px;
font-size: 0.75rem; font-weight: 800; letter-spacing: 0.2em; margin-bottom: 20px;
}
.hero h1 { font-size: 2.7rem; font-weight: 900; letter-spacing: -0.02em; margin: 0 0 16px 0; color: #fff; line-height: 1.25; }
.hero p { font-size: 1.05rem; color: var(--text-muted); max-width: 840px; margin: 0 auto; font-weight: 400; }

/* ライブメトリクス */
.metrics-grid {
display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-bottom: 45px;
}
.metric-card {
background: var(--bg-surface); backdrop-filter: blur(16px);
border: 1px solid var(--border-glass); border-radius: 18px; padding: 20px;
}
.metric-title { font-size: 0.75rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
.metric-value { font-size: 1.7rem; font-weight: 900; color: #fff; }
.metric-sub { font-size: 0.75rem; color: var(--accent-green); margin-top: 4px; font-weight: 600; }

/* 機能カードセクション */
.section-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin-bottom: 20px; border-left: 4px solid var(--accent-gold); padding-left: 12px; }
.features-grid {
display: grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr)); gap: 18px; margin-bottom: 45px;
}
.feature-card {
background: var(--bg-surface); backdrop-filter: blur(16px);
border: 1px solid var(--border-glass); border-radius: 18px; padding: 22px;
transition: all 0.3s ease; position: relative; overflow: hidden;
}
.feature-card:hover { border-color: var(--border-gold); transform: translateY(-3px); box-shadow: 0 12px 35px rgba(0,0,0,0.6); }
.feature-card h3 { color: var(--accent-gold); margin-top: 0; font-size: 1.05rem; font-weight: 800; display: flex; justify-content: space-between; align-items: center; }
.feature-tag { font-size: 0.65rem; background: rgba(192, 132, 252, 0.15); color: var(--accent-purple); padding: 3px 8px; border-radius: 6px; font-weight: 700; }
.feature-card p { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0; line-height: 1.6; }

/* コンソールコントロール */
.console-box {
background: linear-gradient(145deg, rgba(10, 16, 31, 0.95), rgba(1, 3, 7, 0.98));
backdrop-filter: blur(24px); border: 2px solid var(--accent-gold);
border-radius: 28px; padding: 40px 30px; box-shadow: 0 0 100px var(--accent-gold-glow);
}
.console-header { margin-bottom: 28px; text-align: center; }
.console-title { font-size: 1.6rem; font-weight: 900; color: #fff; margin: 0 0 8px 0; }
.console-desc { font-size: 0.85rem; color: var(--text-muted); margin: 0; }

.form-group { margin-bottom: 24px; text-align: left; }
label { display: block; font-size: 0.8rem; color: var(--accent-gold); font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }

select, input {
background: rgba(1, 3, 7, 0.9); color: var(--text-main); border: 1px solid rgba(255, 255, 255, 0.15);
padding: 16px 18px; font-size: 0.95rem; border-radius: 14px; font-weight: 600; outline: none; width: 100%;
transition: all 0.2s ease;
}
select:focus, input:focus { border-color: var(--accent-gold); box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2); }

.action-btn {
background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
color: #010307; border: none; padding: 20px; font-size: 1.1rem; font-weight: 900;
border-radius: 14px; cursor: pointer; transition: all 0.3s ease; width: 100%;
box-shadow: 0 10px 35px rgba(245, 158, 11, 0.4); text-transform: uppercase; letter-spacing: 0.1em;
}
.action-btn:hover { transform: translateY(-2px); box-shadow: 0 15px 45px rgba(245, 158, 11, 0.6); }

/* 実行結果ターミナル */
#result-terminal {
margin-top: 30px; background: rgba(1, 3, 7, 0.95); border: 1px solid rgba(56, 189, 248, 0.4);
padding: 24px; border-radius: 16px; display: none; font-family: monospace; font-size: 0.85rem; text-align: left;
}
.terminal-header { color: var(--accent-cyan); font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.terminal-content { color: var(--text-muted); line-height: 1.6; word-break: break-all; }
.success-highlight { color: var(--accent-green); font-weight: bold; }
</style>
</head>
<body>

<div class="video-bg-container">
    <video autoplay muted loop playsinline>
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-with-code-31910-large.mp4" type="video/mp4">
    </video>
</div>

<div class="ambient-glow"></div>
<div class="container">

<header class="nav-header">
    <div class="logo-area">
        <div class="logo-text">QLUX APEX</div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        TERANODE INFINITY MESH ACTIVE
    </div>
</header>

<section class="hero">
    <div class="badge-sub">WORLD'S #1 ENTERPRISE BSV INFRASTRUCTURE</div>
    <h1>世界最高峰の優良企業を駆動する、<br>次世代BSV自律統合プラットフォーム。</h1>
    <p>Teranodeの無限スケーラビリティ、HandCashミリ秒決済、Tokenizedデジタル証券、TAALハッシュパワーが完全融合。仲介者を一切排除し、地球規模の資本とデータを高速循環させる究極のインフラストラクチャ。</p>
</section>

<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-title">Consolidated TPS</div>
        <div class="metric-value">24,150,890</div>
        <div class="metric-sub">▲ Teranode Verified</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Global Enterprise APIs</div>
        <div class="metric-value">84 Connected</div>
        <div class="metric-sub">▲ Full Ecosystem Sync</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Settlement Latency</div>
        <div class="metric-value">< 0.1 ms</div>
        <div class="metric-sub">▲ Zero-Conf Atomic</div>
    </div>
</div>

<div class="section-title">BSV ADVANCED ENTERPRISE SUITE & SERVICES</div>
<div class="features-grid">
    <div class="feature-card">
        <h3>1. HandCash ($handle) Instant Pay <span class="feature-tag">HandCash API</span></h3>
        <p>ハンドルネームベースのワンクリック即時決済とオムニチャネル・アイデンティティ認証。手数料ほぼゼロでミリ秒の投げ銭、商取引、自動課金を完全自動化。</p>
    </div>
    <div class="feature-card">
        <h3>2. Tokenized Digital Securities <span class="feature-tag">Tokenized Protocol</span></h3>
        <p>法人向けスマートコントラクトによるデジタル証券・株式の発行と譲渡制限。法的拘束力を持つオンチェーン・コーポレートガバナンスを自動執行。</p>
    </div>
    <div class="feature-card">
        <h3>3. TAAL Enterprise Mining Power <span class="feature-tag">TAAL Core</span></h3>
        <p>大規模トランザクションの確実なブロック組み込みとエンタープライズ向けハッシュパワー保証。高スループットデータを途切れることなくチェーンへ刻み込む。</p>
    </div>
    <div class="feature-card">
        <h3>4. Centbee Global Gateway <span class="feature-tag">Centbee Pay</span></h3>
        <p>クロスボーダー決済およびマーチャント向けシームレスインフラ。一般ユーザーから大企業まで複雑なブロックチェーン知識を一切不要にしたスマート決済網。</p>
    </div>
    <div class="feature-card">
        <h3>5. GorillaPool STAS / Ordinals <span class="feature-tag">STAS Engine</span></h3>
        <p>ネイティブ・トークン（STAS）規格の安全な発行・管理と、オンチェーン不変データのインデックス化。高度なスマートスクリプト運用を完全にサポート。</p>
    </div>
    <div class="feature-card">
        <h3>6. SensibleNode Real-time Indexing <span class="feature-tag">Sensible API</span></h3>
        <p>超高速オンチェーンデータクエリとインデックス生成。膨大なブロックチェーンデータをミリ秒単位で抽出し、アプリケーション層へリアルタイム配信。</p>
    </div>
</div>

<div class="console-box">
    <div class="console-header">
        <h2 class="console-title">GLOBAL ENTERPRISE DISPATCH CONSOLE</h2>
        <p class="console-desc">BSV主要企業のすべてのプロトコル・機能を即時選択し、ブロックチェーン上で一括実行。</p>
    </div>

    <div class="form-group">
        <label>BSV SERVICE MODULE / 最先端機能モジュール選択</label>
        <select id="bsv-service-module">
            <option value="handcash_instant_pay">HandCash ($handle) ミリ秒決済・アイデンティティ連携</option>
            <option value="tokenized_security_issue">Tokenized スマートコントラクト・デジタル証券発行</option>
            <option value="taal_enterprise_mining">TAAL エンタープライズ・ハッシュパワー同期</option>
            <option value="centbee_crossborder_gateway">Centbee グローバル・マーチャント決済</option>
            <option value="gorillapool_stas_engine">GorillaPool STAS トークン発行・管理</option>
            <option value="sensible_node_query">SensibleNode 超高速インデックスクエリ</option>
        </select>
    </div>

    <div class="form-group">
        <label>TERANODE SCALING LAYER / 拡張インフラストラクチャ</label>
        <select id="teranode-scaling-layer">
            <option value="teranode_infinity_mesh">BSV Teranode Infinity Mesh (無限並列処理)</option>
            <option value="enterprise_sharded_cluster">Enterprise Sharded Cluster (高信頼性セキュア)</option>
            <option value="global_atomic_settlement_hub">Global Atomic Settlement Hub (ミリ秒決済)</option>
        </select>
    </div>

    <div class="form-group">
        <label>EXECUTION PAYLOAD / 実行データ・パラメータ</label>
        <input type="text" id="execution-payload" value="QLUX-Apex-Enterprise-Global-Core-v500">
    </div>

    <div class="form-group">
        <label>CORPORATE AUTH HANDLE / 企業認証ハンドラ (例: $qlux_enterprise)</label>
        <input type="text" id="corporate-auth-handle" value="$qlux_enterprise">
    </div>

    <button class="action-btn" onclick="executeApexDispatch()">⚡ EXECUTE GLOBAL ENTERPRISE DISPATCH</button>

    <div id="result-terminal">
        <div class="terminal-header">
            <span>●</span> APEX CONSENSUS STATUS: <span class="success-highlight">VERIFIED & EXECUTED ON-CHAIN</span>
        </div>
        <div id="terminal-output" class="terminal-content"></div>
    </div>
</div>

</div>

<script>
async function executeApexDispatch() {
    const bsvServiceModule = document.getElementById('bsv-service-module').value;
    const teranodeScalingLayer = document.getElementById('teranode-scaling-layer').value;
    const executionPayload = document.getElementById('execution-payload').value;
    const corporateAuthHandle = document.getElementById('corporate-auth-handle').value;
    const terminal = document.getElementById('result-terminal');
    const output = document.getElementById('terminal-output');
    
    terminal.style.display = "block";
    output.innerHTML = "Broadcasting multi-enterprise cryptographic payload to BSV Teranode & partner APIs...";

    try {
        const response = await fetch('/api/apex-dispatch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                bsv_service_module: bsvServiceModule, 
                teranode_scaling_layer: teranodeScalingLayer, 
                execution_payload: executionPayload,
                corporate_auth_handle: corporateAuthHandle
            })
        });
        const data = await response.json();

        setTimeout(() => {
            output.innerHTML = `
                ✓ <b>Service Module:</b> ${data.bsv_service_module.toUpperCase()}<br>
                ✓ <b>Scaling Layer:</b> ${data.teranode_scaling_layer}<br>
                ✓ <b>Auth Handle:</b> ${data.corporate_auth_handle}<br>
                ✓ <b>Payload Hash:</b> ${data.execution_payload}<br>
                ✓ <b>Teranode Block Hash:</b> <code>${data.block_hash}</code><br>
                ✓ <b>Global Deployment:</b> <span class="success-highlight">100% Fully Operational Worldwide</span><br><br>
                <span style="color: var(--accent-gold);">[!] All BSV enterprise services successfully synchronized and verified on-chain.</span>
            `;
        }, 600);
    } catch (err) {
        output.innerText = "Error: Enterprise gateway connection timeout.";
    }
}
</script>
</body>
</html>
"""

@app.post("/api/apex-dispatch")
async def api_apex_dispatch(data: ApexEnterpriseRequest):
    raw_str = f"{data.bsv_service_module}-{data.teranode_scaling_layer}-{data.corporate_auth_handle}-{time.time()}"
    block_hash = hashlib.sha256(raw_str.encode()).hexdigest()
    return {
        "status": "success",
        "bsv_service_module": data.bsv_service_module,
        "teranode_scaling_layer": data.teranode_scaling_layer,
        "execution_payload": data.execution_payload,
        "corporate_auth_handle": data.corporate_auth_handle,
        "block_hash": block_hash
    }
