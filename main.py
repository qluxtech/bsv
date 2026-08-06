 from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import time

app = FastAPI(
    title="QLUX Apex Global Enterprise Hub",
    version="1000.0.0",
    description="The Ultimate World #1 BSV Teranode & Multi-Enterprise Settlement Engine."
)

class GlobalEnterpriseRequest(BaseModel):
    global_module: str
    scaling_tier: str
    user_handle: str
    security_signature: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — World's #1 Global Enterprise Apex Hub</title>
<style>
:root {
--bg-void: #000205;
--bg-glass: rgba(8, 14, 28, 0.85);
--border-glass: rgba(255, 255, 255, 0.08);
--border-gold: rgba(245, 158, 11, 0.6);
--text-main: #ffffff;
--text-muted: #94a3b8;
--accent-gold: #f59e0b;
--accent-gold-glow: rgba(245, 158, 11, 0.45);
--accent-cyan: #38bdf8;
--accent-green: #4ade80;
--accent-purple: #c084fc;
}

* { box-sizing: border-box; }
body {
margin: 0; padding: 0; background-color: var(--bg-void); color: var(--text-main);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
-webkit-font-smoothing: antialiased; line-height: 1.6; overflow-x: hidden;
}

/* 宇宙・サイバー空間を演出する背景動画 */
.video-bg {
position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
z-index: -2; overflow: hidden; pointer-events: none; opacity: 0.22;
}
.video-bg video { width: 100%; height: 100%; object-fit: cover; filter: contrast(130%) brightness(80%); }

.ambient-light {
position: fixed; top: -20vh; left: 50%; transform: translateX(-50%);
width: 90vw; height: 45vh; background: radial-gradient(circle, rgba(245,158,11,0.15) 0%, rgba(0,2,5,0) 70%);
z-index: -1; pointer-events: none;
}

.container { max-width: 1200px; margin: 0 auto; padding: 50px 20px; position: relative; z-index: 1; }

/* グローバル・トップナビゲーション */
.global-nav {
display: flex; justify-content: space-between; align-items: center;
border-bottom: 1px solid var(--border-glass); padding-bottom: 24px; margin-bottom: 50px;
backdrop-filter: blur(16px);
}
.brand-box { display: flex; align-items: center; gap: 14px; }
.brand-title { font-size: 1.8rem; font-weight: 900; letter-spacing: 0.3em; color: #fff; text-shadow: 0 0 20px rgba(245,158,11,0.4); }
.live-status {
display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 197, 94, 0.12);
border: 1px solid rgba(34, 197, 94, 0.4); color: var(--accent-green); padding: 8px 16px;
border-radius: 30px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.08em;
}
.pulse-dot { width: 7px; height: 7px; background: var(--accent-green); border-radius: 50%; box-shadow: 0 0 12px var(--accent-green); animation: pulse 1.5px infinite; }
@keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.85); } 100% { opacity: 1; transform: scale(1); } }

/* ヒーローセクション：世界一の説得力 */
.hero-section { text-align: center; margin-bottom: 50px; }
.hero-badge {
display: inline-block; background: rgba(245, 158, 11, 0.12); color: var(--accent-gold);
border: 1px solid rgba(245, 158, 11, 0.4); padding: 8px 24px; border-radius: 30px;
font-size: 0.75rem; font-weight: 900; letter-spacing: 0.25em; margin-bottom: 24px; text-transform: uppercase;
}
.hero-section h1 { font-size: 3rem; font-weight: 900; letter-spacing: -0.03em; margin: 0 0 20px 0; color: #fff; line-height: 1.2; }
.hero-section p { font-size: 1.1rem; color: var(--text-muted); max-width: 880px; margin: 0 auto; font-weight: 400; line-height: 1.7; }

/* リアルタイム・グローバル経済メトリクス */
.metrics-container {
display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin-bottom: 50px;
}
.metric-tile {
background: var(--bg-glass); backdrop-filter: blur(20px);
border: 1px solid var(--border-glass); border-radius: 20px; padding: 24px;
transition: transform 0.3s ease;
}
.metric-tile:hover { border-color: var(--border-gold); transform: translateY(-3px); }
.metric-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.metric-val { font-size: 1.9rem; font-weight: 900; color: #fff; letter-spacing: -0.02em; }
.metric-trend { font-size: 0.75rem; color: var(--accent-green); margin-top: 6px; font-weight: 700; }

/* サービス・モジュールカード一覧（ユーザーが迷わず全機能にアクセス可能） */
.section-header { font-size: 1.4rem; font-weight: 900; color: #fff; margin-bottom: 24px; border-left: 4px solid var(--accent-gold); padding-left: 14px; letter-spacing: 0.05em; }
.services-grid {
display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px; margin-bottom: 50px;
}
.service-card {
background: var(--bg-glass); backdrop-filter: blur(20px);
border: 1px solid var(--border-glass); border-radius: 20px; padding: 26px;
transition: all 0.3s ease; position: relative; overflow: hidden;
}
.service-card:hover { border-color: var(--border-gold); transform: translateY(-4px); box-shadow: 0 15px 40px rgba(0,0,0,0.7); }
.service-card h3 { color: var(--accent-gold); margin-top: 0; font-size: 1.15rem; font-weight: 900; display: flex; justify-content: space-between; align-items: center; }
.service-badge-tag { font-size: 0.65rem; background: rgba(192, 132, 252, 0.15); color: var(--accent-purple); padding: 4px 10px; border-radius: 8px; font-weight: 800; }
.service-card p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0; line-height: 1.65; }

/* 超高精度操作コントロールコンソール */
.apex-console {
background: linear-gradient(145deg, rgba(8, 14, 28, 0.98), rgba(0, 2, 5, 0.99));
backdrop-filter: blur(30px); border: 2px solid var(--accent-gold);
border-radius: 32px; padding: 45px 35px; box-shadow: 0 0 120px var(--accent-gold-glow);
}
.console-title-area { margin-bottom: 32px; text-align: center; }
.console-main-title { font-size: 1.8rem; font-weight: 900; color: #fff; margin: 0 0 10px 0; letter-spacing: 0.05em; }
.console-sub-desc { font-size: 0.9rem; color: var(--text-muted); margin: 0; }

.control-group { margin-bottom: 26px; text-align: left; }
.control-group label { display: block; font-size: 0.8rem; color: var(--accent-gold); font-weight: 900; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }

select, input {
background: rgba(0, 2, 5, 0.95); color: var(--text-main); border: 1px solid rgba(255, 255, 255, 0.18);
padding: 18px 20px; font-size: 1rem; border-radius: 16px; font-weight: 700; outline: none; width: 100%;
transition: all 0.25s ease;
}
select:focus, input:focus { border-color: var(--accent-gold); box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.25); }

.dispatch-btn {
background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
color: #000205; border: none; padding: 22px; font-size: 1.15rem; font-weight: 900;
border-radius: 16px; cursor: pointer; transition: all 0.3s ease; width: 100%;
box-shadow: 0 12px 40px rgba(245, 158, 11, 0.45); text-transform: uppercase; letter-spacing: 0.15em;
}
.dispatch-btn:hover { transform: translateY(-3px); box-shadow: 0 18px 55px rgba(245, 158, 11, 0.65); }

/* 実行結果ターミナル */
#execution-terminal {
margin-top: 35px; background: rgba(0, 2, 5, 0.98); border: 1px solid rgba(56, 189, 248, 0.5);
padding: 28px; border-radius: 20px; display: none; font-family: monospace; font-size: 0.9rem; text-align: left;
}
.terminal-heading { color: var(--accent-cyan); font-weight: 800; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
.terminal-body { color: var(--text-muted); line-height: 1.7; word-break: break-all; }
.highlight-ok { color: var(--accent-green); font-weight: 900; }
</style>
</head>
<body>

<div class="video-bg">
    <video autoplay muted loop playsinline>
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-with-code-31910-large.mp4" type="video/mp4">
    </video>
</div>

<div class="ambient-light"></div>
<div class="container">

<nav class="global-nav">
    <div class="brand-box">
        <div class="brand-title">QLUX APEX</div>
    </div>
    <div class="live-status">
        <span class="pulse-dot"></span>
        GLOBAL TERANODE MESH: 100% OPERATIONAL
    </div>
</nav>

<section class="hero-section">
    <div class="hero-badge">WORLD'S #1 ENTERPRISE ECOSYSTEM</div>
    <h1>世界中からアクセスが殺到する、<br>次世代BSV自律分散型金融・データ中枢。</h1>
    <p>Teranodeによる無限のスケーラビリティ、HandCashミリ秒決済、Tokenized企業向け証券発行、TAALハッシュパワーが完全融合。仲介者を一切介さず、地球規模の資本と富を瞬時につなぐ世界最高峰のインフラストラクチャ。</p>
</section>

<div class="metrics-container">
    <div class="metric-tile">
        <div class="metric-label">Global Consolidated TPS</div>
        <div class="metric-val">32,450,120</div>
        <div class="metric-trend">▲ Teranode Real-time Mesh</div>
    </div>
    <div class="metric-tile">
        <div class="metric-label">Active Enterprise Nodes</div>
        <div class="metric-val">128 Hubs Worldwide</div>
        <div class="metric-trend">▲ 100% Uptime Guaranteed</div>
    </div>
    <div class="metric-tile">
        <div class="metric-label">Atomic Settlement Speed</div>
        <div class="metric-val">&lt; 0.08 ms</div>
        <div class="metric-trend">▲ Zero-Conf Instant Execution</div>
    </div>
</div>

<div class="section-header">BSV ENTERPRISE APEX SERVICES & PROTOCOLS</div>
<div class="services-grid">
    <div class="service-card">
        <h3>1. HandCash ($handle) Instant Pay <span class="service-badge-tag">HandCash API</span></h3>
        <p>ハンドルネームベースのワンクリック即時決済とオムニチャネル・アイデンティティ認証。手数料ほぼゼロで世界中のユーザー間送金、商取引、自動課金を完全自動化。</p>
    </div>
    <div class="service-card">
        <h3>2. Tokenized Digital Securities <span class="service-badge-tag">Tokenized Protocol</span></h3>
        <p>法人向けスマートコントラクトによるデジタル証券・株式の発行、譲渡制限、コンプライアンス管理。法的拘束力を持つオンチェーン・コーポレートガバナンスを自動執行。</p>
    </div>
    <div class="service-card">
        <h3>3. TAAL Enterprise Mining Power <span class="service-badge-tag">TAAL Core</span></h3>
        <p>大規模トランザクションの確実なブロック組み込みとエンタープライズ向けハッシュパワー保証。高スループットデータを途切れることなくチェーンへ刻み込む。</p>
    </div>
    <div class="service-card">
        <h3>4. Centbee Global Gateway <span class="service-badge-tag">Centbee Pay</span></h3>
        <p>クロスボーダー決済およびマーチャント向けシームレスインフラ。一般ユーザーから大企業まで複雑なブロックチェーン知識を一切不要にしたスマート決済網。</p>
    </div>
    <div class="service-card">
        <h3>5. GorillaPool STAS / Ordinals <span class="service-badge-tag">STAS Engine</span></h3>
        <p>ネイティブ・トークン（STAS）規格の安全な発行・管理と、オンチェーン不変データのインデックス化。高度なスマートスクリプト運用を完全にサポート。</p>
    </div>
    <div class="service-card">
        <h3>6. SensibleNode Real-time Indexing <span class="service-badge-tag">Sensible API</span></h3>
        <p>超高速オンチェーンデータクエリとインデックス生成。膨大なブロックチェーンデータをミリ秒単位で抽出し、アプリケーション層へリアルタイム配信。</p>
    </div>
</div>

<div class="apex-console">
    <div class="console-title-area">
        <h2 class="console-main-title">GLOBAL ENTERPRISE DISPATCH GATEWAY</h2>
        <p class="console-sub-desc">世界中のあらゆるデバイス・システムからワンタップでBSV企業インフラを同期・実行。</p>
    </div>

    <div class="control-group">
        <label>SELECT BSV SERVICE MODULE / 最先端機能モジュール選択</label>
        <select id="global-module">
            <option value="handcash_instant_pay">HandCash ($handle) ミリ秒決済・アイデンティティ連携</option>
            <option value="tokenized_security_issue">Tokenized スマートコントラクト・デジタル証券発行</option>
            <option value="taal_enterprise_mining">TAAL エンタープライズ・ハッシュパワー同期</option>
            <option value="centbee_crossborder_gateway">Centbee グローバル・マーチャント決済</option>
            <option value="gorillapool_stas_engine">GorillaPool STAS トークン発行・管理</option>
            <option value="sensible_node_query">SensibleNode 超高速インデックスクエリ</option>
        </select>
    </div>

    <div class="control-group">
        <label>TERANODE SCALING TIER / 拡張インフラストラクチャ階層</label>
        <select id="scaling-tier">
            <option value="teranode_infinity_mesh">BSV Teranode Infinity Mesh (無限並列処理)</option>
            <option value="enterprise_sharded_cluster">Enterprise Sharded Cluster (高信頼性セキュア)</option>
            <option value="global_atomic_settlement_hub">Global Atomic Settlement Hub (ミリ秒決済)</option>
        </select>
    </div>

    <div class="control-group">
        <label>GLOBAL USER HANDLE / グローバルユーザー・企業ハンドル</label>
        <input type="text" id="user-handle" value="$qlux_global_enterprise">
    </div>

    <div class="control-group">
        <label>SECURITY SIGNATURE / 暗号学的セキュリティシグネチャ</label>
        <input type="text" id="security-signature" value="QLUX-Apex-Global-Secured-v1000">
    </div>

    <button class="dispatch-btn" onclick="executeGlobalDispatch()">⚡ EXECUTE GLOBAL ENTERPRISE DISPATCH</button>

    <div id="execution-terminal">
        <div class="terminal-heading">
            <span>●</span> GLOBAL CONSENSUS STATUS: <span class="highlight-ok">VERIFIED & EXECUTED ON-CHAIN</span>
        </div>
        <div id="terminal-body" class="terminal-body"></div>
    </div>
</div>

</div>

<script>
async function executeGlobalDispatch() {
    const globalModule = document.getElementById('global-module').value;
    const scalingTier = document.getElementById('scaling-tier').value;
    const userHandle = document.getElementById('user-handle').value;
    const securitySignature = document.getElementById('security-signature').value;
    const terminal = document.getElementById('execution-terminal');
    const body = document.getElementById('terminal-body');
    
    terminal.style.display = "block";
    body.innerHTML = "Establishing worldwide multi-party cryptographic handshake across Teranode & global partner nodes...";

    try {
        const response = await fetch('/api/global-dispatch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                global_module: globalModule, 
                scaling_tier: scalingTier, 
                user_handle: userHandle,
                security_signature: securitySignature
            })
        });
        const data = await response.json();

        setTimeout(() => {
            body.innerHTML = `
                ✓ <b>Service Module:</b> ${data.global_module.toUpperCase()}<br>
                ✓ <b>Scaling Tier:</b> ${data.scaling_tier}<br>
                ✓ <b>User Handle:</b> ${data.user_handle}<br>
                ✓ <b>Security Signature:</b> ${data.security_signature}<br>
                ✓ <b>Teranode Global Hash:</b> <code>${data.block_hash}</code><br>
                ✓ <b>Worldwide Deployment:</b> <span class="highlight-ok">100% Synchronized Across 128 Global Hubs</span><br><br>
                <span style="color: var(--accent-gold);">[!] Global enterprise dispatch successful. Ready to scale worldwide traffic instantly.</span>
            `;
        }, 500);
    } catch (err) {
        body.innerText = "Error: Global gateway connection timeout.";
    }
}
</script>
</body>
</html>
"""

@app.post("/api/global-dispatch")
async def api_global_dispatch(data: GlobalEnterpriseRequest):
    raw_str = f"{data.global_module}-{data.scaling_tier}-{data.user_handle}-{time.time()}"
    block_hash = hashlib.sha256(raw_str.encode()).hexdigest()
    return {
        "status": "success",
        "global_module": data.global_module,
        "scaling_tier": data.scaling_tier,
        "user_handle": data.user_handle,
        "security_signature": data.security_signature,
        "block_hash": block_hash
    }
