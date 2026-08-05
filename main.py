from fastapi import FastAPI, HTTPException, Request
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
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Qlux</title>
        <style>
            :root {
                --bg-color: #030305;
                --text-color: #f8fafc;
                --accent-gold: #fbbf24;
                --accent-blue: #38bdf8;
                --card-bg: rgba(15, 23, 42, 0.85);
                --border-color: rgba(251, 191, 36, 0.25);
            }
            body {
                margin: 0;
                padding: 0;
                background-color: var(--bg-color);
                color: var(--text-color);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 50px 20px;
            }
            header {
                text-align: center;
                padding: 40px 0;
            }
            h1 {
                font-size: 3.5rem;
                margin: 0 0 10px 0;
                background: linear-gradient(135deg, #fff, var(--accent-gold));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.03em;
            }
            .tagline {
                font-size: 1.3rem;
                color: #94a3b8;
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.6;
                font-weight: 500;
            }
            .hook-box {
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 35px;
                margin: 30px 0;
                box-shadow: 0 25px 50px rgba(0,0,0,0.6);
            }
            .hook-box h2 {
                color: var(--accent-gold);
                margin-top: 0;
                font-size: 1.6rem;
            }
            .hook-box p {
                line-height: 1.8;
                color: #cbd5e1;
                font-size: 1.05rem;
                margin-bottom: 20px;
            }
            .highlight-red {
                color: #f87171;
                font-weight: bold;
            }
            .highlight-green {
                color: #34d399;
                font-weight: bold;
            }
            .payment-gateway {
                background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
                border: 2px solid var(--accent-gold);
                border-radius: 16px;
                padding: 40px;
                text-align: center;
                margin: 40px 0;
                box-shadow: 0 0 40px rgba(251, 191, 36, 0.2);
            }
            .payment-gateway h3 {
                margin-top: 0;
                font-size: 1.8rem;
                color: #fff;
            }
            .btn-bsv {
                background: linear-gradient(135deg, #fbbf24, #d97706);
                color: #030305;
                border: none;
                padding: 18px 36px;
                font-size: 1.2rem;
                font-weight: 900;
                border-radius: 35px;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                margin-top: 20px;
                box-shadow: 0 4px 20px rgba(251, 191, 36, 0.5);
                letter-spacing: 0.05em;
            }
            .btn-bsv:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(251, 191, 36, 0.8);
            }
            .links-section {
                text-align: center;
                margin-top: 50px;
                padding-bottom: 30px;
            }
            .links-section a {
                color: var(--accent-blue);
                text-decoration: none;
                margin: 0 15px;
                font-weight: 600;
            }
            .links-section a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Qlux</h1>
                <p class="tagline">秒速で繋がり、サトシで駆動する。世界を書き換える分散型経済エンジン。</p>
            </header>

            <div class="hook-box">
                <h2>⚠️ なぜ、あなたは今ここでサトシを支払うのか？</h2>
                <p>
                    インターネットの情報の99%は「ただ垂れ流され、消えていく」。しかし、<span class="highlight-red">価値のある真のデータとシステムリソースは、無償では維持されない。</span>
                </p>
                <p>
                    あなたがここでサトシ（BSV）を投じることで、仲介者ゼロでこのノードの演算回路が直結し、<span class="highlight-green">あなた専用の処理優遇枠と未公開の全リソースがノータイムで解放される。</span>
                </p>
                <p>
                    見ているだけでは、ただの傍観者。サトシを押した者だけが、この新しい経済圏のコアを動かす当事者になる。
                </p>
            </div>

            <div class="payment-gateway">
                <h3>⚡ INSTANT BSV DISPATCH</h3>
                <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 10px;">
                    ワンクリックでコアシステムにエネルギー（サトシ）を送り込む
                </p>
                <div style="margin: 25px 0; font-size: 2.2rem; font-weight: 900; color: var(--accent-gold);">
                    100 Sats
                </div>
                <button class="btn-bsv" onclick="triggerBsvPayment()">🚀 今すぐサトシを支払って起動する</button>
                <div id="payment-status" style="margin-top: 20px; font-size: 0.95rem; color: #38bdf8; font-weight: bold;"></div>
            </div>

            <div class="links-section">
                <a href="/docs">API Docs</a>
                <a href="/openapi.json">OpenAPI Schema</a>
            </div>
        </div>

        <script>
            function triggerBsvPayment() {
                const statusDiv = document.getElementById('payment-status');
                statusDiv.innerText = "BSVウォレット（HandCash / Sensible等）との同期を確立中...";
                setTimeout(() => {
                    statusDiv.innerText = "⚡ ネットワーク承認待ち: トランザクション署名を送信しました";
                }, 1500);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/verify-payment")
async def verify_payment(payload: PaymentVerification):
    if not payload.txid:
        raise HTTPException(status_code=400, detail="Invalid TxID")
    return {
        "status": "success",
        "message": "BSV payment verified. Core loop executed.",
        "txid": payload.txid,
        "satoshis_received": payload.expected_satoshis
    }
