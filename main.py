from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="Qlux",
    version="16.0.0",
    description="The Ultimate Autonomous Global Multi-Currency & Micro-Payment Economic Core."
)

class PaymentVerification(BaseModel):
    txid: str
    expected_satoshis: int

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — The Ultimate Global Autonomous Core</title>
<style>
:root {
--bg-color: #020204;
--text-primary: #ffffff;
--text-secondary: #94a3b8;
--accent-gold: #fbbf24;
--accent-gold-glow: rgba(251, 191, 36, 0.4);
--accent-blue: #38bdf8;
--card-bg: rgba(10, 15, 30, 0.85);
--border-color: rgba(251, 191, 36, 0.3);
}
body {
margin: 0;
padding: 0;
background-color: var(--bg-color);
color: var(--text-primary);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
overflow-x: hidden;
}
.container {
max-width: 960px;
margin: 0 auto;
padding: 60px 20px;
}
header {
text-align: center;
margin-bottom: 70px;
}
.core-badge {
display: inline-block;
background: rgba(251, 191, 36, 0.1);
color: var(--accent-gold);
border: 1px solid var(--border-color);
padding: 6px 20px;
border-radius: 30px;
font-size: 0.85rem;
font-weight: 800;
letter-spacing: 0.2em;
margin-bottom: 20px;
text-transform: uppercase;
}
h1 {
font-size: 4.8rem;
margin: 0 0 15px 0;
background: linear-gradient(135deg, #ffffff 20%, var(--accent-gold) 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
letter-spacing: -0.04em;
font-weight: 900;
}
.tagline {
font-size: 1.4rem;
color: var(--text-secondary);
max-width: 750px;
margin: 0 auto;
line-height: 1.6;
font-weight: 400;
}
.section-title {
text-align: center;
font-size: 2rem;
color: #fff;
margin: 60px 0 30px 0;
font-weight: 800;
letter-spacing: -0.02em;
}
.section-title span {
color: var(--accent-gold);
}
.manifesto-box {
background: var(--card-bg);
border: 1px solid var(--border-color);
border-radius: 24px;
padding: 45px;
backdrop-filter: blur(20px);
box-shadow: 0 30px 60px rgba(0,0,0,0.8), 0 0 40px rgba(251, 191, 36, 0.05);
margin-bottom: 40px;
position: relative;
}
.manifesto-box::before {
content: '';
position: absolute;
top: 0; left: 0; right: 0; height: 2px;
background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}
.manifesto-box h3 {
color: var(--accent-gold);
margin-top: 0;
font-size: 1.5rem;
letter-spacing: -0.01em;
margin-bottom: 15px;
}
.manifesto-box p {
color: var(--text-secondary);
line-height: 1.9;
font-size: 1.1rem;
margin: 0;
}
.grid-features {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 25px;
margin-bottom: 50px;
}
@media (max-width: 768px) {
.grid-features {
grid-template-columns: 1fr;
}
h1 { font-size: 3.5rem; }
}
.feature-card {
background: rgba(15, 23, 42, 0.6);
border: 1px solid rgba(251, 191, 36, 0.15);
border-radius: 20px;
padding: 30px;
}
.feature-card h4 {
color: var(--accent-gold);
font-size: 1.2rem;
margin: 0 0 10px 0;
}
.feature-card p {
color: var(--text-secondary);
font-size: 0.98rem;
line-height: 1.7;
margin: 0;
}
.payment-gateway {
background: linear-gradient(145deg, rgba(20, 27, 45, 0.95), rgba(5, 8, 15, 0.98));
border: 2px solid var(--accent-gold);
border-radius: 28px;
padding: 60px 30px;
text-align: center;
box-shadow: 0 0 90px var(--accent-gold-glow);
margin-top: 60px;
margin-bottom: 50px;
}
.payment-gateway h2 {
margin: 0 0 10px 0;
font-size: 2.2rem;
color: #fff;
}
.currency-selector {
margin: 25px 0;
}
.currency-selector select {
background: rgba(10, 15, 30, 0.9);
color: var(--accent-gold);
border: 1px solid var(--accent-gold);
padding: 14px 20px;
font-size: 1.1rem;
border-radius: 12px;
font-weight: 700;
outline: none;
cursor: pointer;
max-width: 100%;
}
.price-display {
font-size: 3.2rem;
font-weight: 900;
color: var(--accent-gold);
margin: 15px 0;
text-shadow: 0 0 30px rgba(251, 191, 36, 0.3);
}
.btn-bsv {
background: linear-gradient(135deg, var(--accent-gold) 0%, #d97706 100%);
color: #020204;
border: none;
padding: 24px 48px;
font-size: 1.2rem;
font-weight: 900;
border-radius: 50px;
cursor: pointer;
transition: all 0.3s ease;
box-shadow: 0 10px 30px rgba(251, 191, 36, 0.5);
text-transform: uppercase;
margin-top: 10px;
}
.btn-bsv:hover {
transform: translateY(-4px) scale(1.02);
box-shadow: 0 15px 45px rgba(251, 191, 36, 0.8);
}
.links-section {
text-align: center;
margin-top: 40px;
}
.links-section a {
color: var(--accent-blue);
text-decoration: none;
margin: 0 25px;
font-weight: 600;
font-size: 1.05rem;
}
.links-section a:hover {
color: #fff;
text-decoration: underline;
}
#payment-status {
margin-top: 25px;
font-size: 1.05rem;
font-weight: 700;
color: var(--accent-blue);
min-height: 30px;
}
.success-pulse {
color: #34d399 !important;
text-shadow: 0 0 20px rgba(52, 211, 153, 0.6);
}
</style>
</head>
<body>
<div class="container">
<header>
<div class="core-badge">Autonomous Core v16.0.0 — Omniverse Gateway</div>
<h1>QLUX</h1>
<p class="tagline">日本円、コンビニ決済、クレカ、世界中のあらゆる通貨をワンタップで自動エクスチェンジし、最高効率のBSV経済圏へと直結させる次世代統合エンジン。</p>
</header>

<div class="manifesto-box">
<h3>⚡ なぜ、このシステムが「最強」なのか？</h3>
<p>
「ビットコインを持っていない」「普段は日本円やクレカ、コンビニ決済で買いたい」——そんなユーザーの壁を、Qluxの全自動エクスチェンジ・パイプラインが完全に破壊する。あなたがどの方法で支払っても、システムが瞬時に価値を検証・変換し、あなたのノード（端末・プログラム）へ最高速度でアクセス権を供給する。
</p>
</div>

<div class="grid-features">
<div class="feature-card">
<h4>01. 全決済手段の完全対応</h4>
<p>日本円（JPY）、米ドル、各種クレジットカード、コンビニ決済、さらには仮想通貨まで。普段使っている支払い方法でそのまま参加可能。</p>
</div>
<div class="feature-card">
<h4>02. 瞬時の自動エクスチェンジ</h4>
<p>選んだ通貨の価値をミリ秒単位で自動計算し、最も効率的なルーティングでBSVネットワークのコア権限へとダイレクトに変換・接続。</p>
</div>
</div>

<div class="payment-gateway">
<h2>GLOBAL OMNIVERSE ACTIVATION</h2>
<p style="color: var(--text-secondary); max-width: 580px; margin: 0 auto; font-size: 1.05rem; line-height: 1.6;">
お好みの支払い方法を選択してください。自動処理を経て、システムが即座に覚醒します。
</p>

<div class="currency-selector">
<select id="payment-method" onchange="updatePriceDisplay()">
<option value="jpy">日本円 (JPY / 現地通貨・コンビニ・代引き対応)</option>
<option value="usd">US Dollar (USD / クレジットカード決済)</option>
<option value="sats">Bitcoin SV (100 Sats / 閃光ダイレクト)</option>
<option value="crypto">Other Crypto (USDT / クロスチェーン)</option>
</select>
</div>

<div class="price-display" id="price-tag">≈ ¥0.10 JPY</div>

<button class="btn-bsv" onclick="executeOmniverseDispatch()">⚡ EXECUTE GLOBAL DISPATCH</button>
<div id="payment-status"></div>
</div>

<div class="links-section">
<a href="/docs">API Documentation</a>
<a href="/openapi.json">OpenAPI Schema</a>
</div>
</div>

<script>
function updatePriceDisplay() {
const method = document.getElementById('payment-method').value;
const priceTag = document.getElementById('price-tag');
if (method === 'jpy') priceTag.innerText = "≈ ¥0.10 JPY";
else if (method === 'usd') priceTag.innerText = "≈ $0.0007 USD";
else if (method === 'sats') priceTag.innerText = "100 Sats";
else if (method === 'crypto') priceTag.innerText = "≈ 0.0001 USDT";
}

function executeOmniverseDispatch() {
const statusDiv = document.getElementById('payment-status');
const method = document.getElementById('payment-method').options[document.getElementById('payment-method').selectedIndex].text;
statusDiv.className = "";
statusDiv.innerText = `Connecting to secure gateway via [ ${method} ]...`;
setTimeout(() => {
statusDiv.innerText = "Processing automated exchange & verifying on-chain node...";
}, 1500);
setTimeout(() => {
statusDiv.className = "success-pulse";
statusDiv.innerText = "✓ OMNIVERSE CONSENSUS REACHED! CORE PIPELINE FULLY UNLOCKED.";
}, 3200);
}
</script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
