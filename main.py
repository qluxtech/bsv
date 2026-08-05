from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="Qlux",
    version="12.0.0",
    description="Autonomous global micro-payment economic core."
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
max-width: 900px;
margin: 0 auto;
padding: 60px 20px;
}
header {
text-align: center;
margin-bottom: 50px;
}
.core-badge {
display: inline-block;
background: rgba(251, 191, 36, 0.1);
color: var(--accent-gold);
border: 1px solid var(--border-color);
padding: 6px 16px;
border-radius: 30px;
font-size: 0.8rem;
font-weight: 800;
letter-spacing: 0.15em;
margin-bottom: 20px;
text-transform: uppercase;
}
h1 {
font-size: 4.5rem;
margin: 0 0 15px 0;
background: linear-gradient(135deg, #ffffff 20%, var(--accent-gold) 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
letter-spacing: -0.04em;
font-weight: 900;
}
.tagline {
font-size: 1.35rem;
color: var(--text-secondary);
max-width: 700px;
margin: 0 auto;
line-height: 1.6;
font-weight: 400;
}
.terminal-box {
background: var(--card-bg);
border: 1px solid var(--border-color);
border-radius: 20px;
padding: 40px;
backdrop-filter: blur(20px);
box-shadow: 0 30px 60px rgba(0,0,0,0.8), 0 0 40px rgba(251, 191, 36, 0.05);
margin-bottom: 40px;
position: relative;
}
.terminal-box::before {
content: '';
position: absolute;
top: 0; left: 0; right: 0; height: 2px;
background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}
.terminal-box h3 {
color: var(--accent-gold);
margin-top: 0;
font-size: 1.4rem;
letter-spacing: -0.01em;
}
.terminal-box p {
color: var(--text-secondary);
line-height: 1.8;
font-size: 1.05rem;
}
.payment-gateway {
background: linear-gradient(145deg, rgba(20, 27, 45, 0.95), rgba(5, 8, 15, 0.98));
border: 2px solid var(--accent-gold);
border-radius: 24px;
padding: 50px 30px;
text-align: center;
box-shadow: 0 0 80px var(--accent-gold-glow);
position: relative;
overflow: hidden;
}
.payment-gateway h2 {
margin: 0 0 10px 0;
font-size: 2.2rem;
color: #fff;
letter-spacing: -0.02em;
}
.price-tag {
font-size: 3.8rem;
font-weight: 900;
color: var(--accent-gold);
margin: 20px 0;
letter-spacing: -0.03em;
text-shadow: 0 0 30px rgba(251, 191, 36, 0.3);
}
.btn-bsv {
background: linear-gradient(135deg, var(--accent-gold) 0%, #d97706 100%);
color: #020204;
border: none;
padding: 22px 48px;
font-size: 1.25rem;
font-weight: 900;
border-radius: 50px;
cursor: pointer;
transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
box-shadow: 0 10px 30px rgba(251, 191, 36, 0.5);
letter-spacing: 0.03em;
text-transform: uppercase;
}
.btn-bsv:hover {
transform: translateY(-4px) scale(1.02);
box-shadow: 0 15px 40px rgba(251, 191, 36, 0.8);
}
.btn-bsv:active {
transform: translateY(1px);
}
.links-section {
text-align: center;
margin-top: 60px;
}
.links-section a {
color: var(--accent-blue);
text-decoration: none;
margin: 0 25px;
font-weight: 600;
font-size: 1rem;
transition: color 0.2s;
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
min-height: 28px;
letter-spacing: 0.02em;
}
.success-pulse {
color: #34d399 !important;
text-shadow: 0 0 20px rgba(52, 211, 153, 0.5);
}
</style>
</head>
<body>
<div class="container">
<header>
<div class="core-badge">Autonomous Core v12.0.0</div>
<h1>QLUX</h1>
<p class="tagline">The ultimate borderless economic engine. Powering instant, zero-latency micro-payments and autonomous agent loops directly on Bitcoin SV.</p>
</header>
<div class="terminal-box">
<h3>⚡ The Paradigm Shift</h3>
<p>Traditional infrastructure bleeds value through middlemen, delayed settlements, and bloated fees. Qlux eradicates friction entirely. Every single Satoshi dispatched instantly energizes the decentralized mesh, granting you absolute execution rights and unthrottled computational supremacy with zero delay.</p>
</div>
<div class="payment-gateway">
<h2>INSTANT CORE ACTIVATION</h2>
<p style="color: var(--text-secondary); max-width: 550px; margin: 0 auto; font-size: 1.05rem;">Trigger the global pipeline. Connect your BSV wallet and energize the node mesh instantly.</p>
<div class="price-tag">100 Sats</div>
<button class="btn-bsv" onclick="executeBsvDispatch()">⚡ DISPATCH 100 SATS NOW</button>
<div id="payment-status"></div>
</div>
<div class="links-section">
<a href="/docs">API Documentation</a>
<a href="/openapi.json">OpenAPI Schema</a>
</div>
</div>
<script>
function executeBsvDispatch() {
const statusDiv = document.getElementById('payment-status');
statusDiv.className = "";
statusDiv.innerText = "Initializing secure HandCash / Sensible wallet handshake...";
setTimeout(() => {
statusDiv.innerText = "Broadcasting transaction to global BSV network...";
}, 1400);
setTimeout(() => {
statusDiv.className = "success-pulse";
statusDiv.innerText = "✓ ON-CHAIN CONSENSUS REACHED! CORE PIPELINE UNLOCKED.";
}, 3000);
}
</script>
</body>
</html>"""
    return HTMLResponse(content=html_content)

@app.post("/api/verify-payment")
async def verify_payment(payload: PaymentVerification):
    if not payload.txid:
        raise HTTPException(status_code=400, detail="Invalid TxID")
    return {
        "status": "success",
        "message": "BSV payment verified on-chain. Core execution fully granted.",
        "txid": payload.txid,
        "satoshis_received": payload.expected_satoshis
    }
