from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="Qlux Instant Core",
    version="18.0.0",
    description="The Ultimate Zero-Friction Instant Simulation Core."
)

class DispatchVerify(BaseModel):
    mode: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — Instant Autonomous Core</title>
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
.container { max-width: 800px; margin: 0 auto; padding: 60px 20px; text-align: center; }
.badge {
display: inline-block; background: rgba(251, 191, 36, 0.1); color: var(--accent-gold);
border: 1px solid rgba(251, 191, 36, 0.3); padding: 6px 20px; border-radius: 30px;
font-size: 0.85rem; font-weight: 800; letter-spacing: 0.2em; margin-bottom: 20px;
}
h1 { font-size: 4rem; margin: 0 0 10px 0; font-weight: 900; }
.gateway {
background: linear-gradient(145deg, rgba(20, 27, 45, 0.95), rgba(5, 8, 15, 0.98));
border: 2px solid var(--accent-gold); border-radius: 28px; padding: 50px 30px;
box-shadow: 0 0 80px var(--accent-gold-glow); margin-top: 40px;
}
select {
background: rgba(10, 15, 30, 0.9); color: var(--accent-gold); border: 1px solid var(--accent-gold);
padding: 14px 20px; font-size: 1.1rem; border-radius: 12px; font-weight: 700; outline: none; cursor: pointer;
margin: 20px 0; width: 100%; max-width: 450px;
}
.btn {
background: linear-gradient(135deg, var(--accent-gold) 0%, #d97706 100%);
color: #020204; border: none; padding: 22px 45px; font-size: 1.2rem; font-weight: 900;
border-radius: 50px; cursor: pointer; transition: all 0.3s ease;
box-shadow: 0 10px 30px rgba(251, 191, 36, 0.5); text-transform: uppercase; display: block; margin: 20px auto 0 auto;
}
.btn:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(251, 191, 36, 0.8); }
#status { margin-top: 25px; font-size: 1.1rem; font-weight: 700; color: var(--accent-blue); min-height: 30px; }
.success { color: #34d399 !important; text-shadow: 0 0 20px rgba(52, 211, 153, 0.6); }
</style>
</head>
<body>
<div class="container">
<div class="badge">Zero-Friction Engine v18.0</div>
<h1>QLUX</h1>
<p style="color: var(--text-secondary);">面倒な手続きは一切不要。ワンタップで全ルートを即時貫通させる。</p>

<div class="gateway">
<h2>INSTANT DISPATCH GATEWAY</h2>
<select id="mode">
<option value="jpy">日本円 / クレカ・コンビニ・代引き (即時変換)</option>
<option value="bsv">Bitcoin SV (100 Sats 閃光直結)</option>
<option value="crypto">Other Crypto / クロスチェーン自動スワップ</option>
</select>

<button class="btn" onclick="executeFast()">⚡ EXECUTE INSTANT DISPATCH</button>
<div id="status"></div>
</div>
</div>

<script>
function executeFast() {
const status = document.getElementById('status');
status.className = "";
status.innerText = "Bypassing external friction & routing through core...";
setTimeout(() => {
status.className = "success";
status.innerText = "✓ INSTANT CONSENSUS REACHED! CORE PIPELINE FULLY UNLOCKED.";
}, 900);
}
</script>
</body>
</html>
"""

@app.post("/api/dispatch")
async def api_dispatch(data: DispatchVerify):
    return {"status": "success", "message": "Instant core execution granted."}
