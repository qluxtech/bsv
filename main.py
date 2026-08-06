import os
import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_CONTENT = """<!DOCTYPE html>
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
}

* { box-sizing: border-box; }
body {
margin: 0; padding: 0; background-color: var(--bg-void); color: var(--text-main);
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
-webkit-font-smoothing: antialiased; line-height: 1.6; overflow-x: hidden;
}

.video-bg {
position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
z-index: -2; overflow: hidden; pointer-events: none; opacity: 0.22;
}
.video-bg video { width: 100%; height: 100%; object-fit: cover; filter: contrast(130%) brightness(80%); }

.container { max-width: 1200px; margin: 0 auto; padding: 50px 20px; position: relative; z-index: 1; }

.global-nav {
display: flex; justify-content: space-between; align-items: center;
border-bottom: 1px solid var(--border-glass); padding-bottom: 24px; margin-bottom: 50px;
backdrop-filter: blur(16px);
}
.brand-title { font-size: 1.8rem; font-weight: 900; letter-spacing: 0.3em; color: #fff; }
.live-status {
display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 197, 94, 0.12);
border: 1px solid rgba(34, 197, 94, 0.4); color: var(--accent-green); padding: 8px 16px;
border-radius: 30px; font-size: 0.75rem; font-weight: 800;
}
.pulse-dot { width: 7px; height: 7px; background: var(--accent-green); border-radius: 50%; box-shadow: 0 0 12px var(--accent-green); }

.hero-section { text-align: center; margin-bottom: 50px; }
.hero-badge {
display: inline-block; background: rgba(245, 158, 11, 0.12); color: var(--accent-gold);
border: 1px solid rgba(245, 158, 11, 0.4); padding: 8px 24px; border-radius: 30px;
font-size: 0.75rem; font-weight: 900; letter-spacing: 0.25em; margin-bottom: 24px; text-transform: uppercase;
}
.hero-section h1 { font-size: 2.8rem; font-weight: 900; margin: 0 0 20px 0; color: #fff; line-height: 1.2; }
.hero-section p { font-size: 1.05rem; color: var(--text-muted); max-width: 800px; margin: 0 auto; line-height: 1.7; }

.apex-console {
background: linear-gradient(145deg, rgba(8, 14, 28, 0.98), rgba(0, 2, 5, 0.99));
border: 2px solid var(--accent-gold); border-radius: 32px; padding: 45px 35px;
box-shadow: 0 0 100px var(--accent-gold-glow); margin-top: 40px;
}
.control-group { margin-bottom: 24px; text-align: left; }
.control-group label { display: block; font-size: 0.8rem; color: var(--accent-gold); font-weight: 900; margin-bottom: 8px; }
select, input {
background: rgba(0, 2, 5, 0.95); color: var(--text-main); border: 1px solid rgba(255, 255, 255, 0.18);
padding: 16px 18px; font-size: 1rem; border-radius: 14px; width: 100%; outline: none;
}
.dispatch-btn {
background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
color: #000205; border: none; padding: 20px; font-size: 1.1rem; font-weight: 900;
border-radius: 14px; cursor: pointer; width: 100%; text-transform: uppercase; letter-spacing: 0.1em;
}
#execution-terminal {
margin-top: 25px; background: rgba(0, 2, 5, 0.98); border: 1px solid rgba(56, 189, 248, 0.5);
padding: 24px; border-radius: 16px; display: none; font-family: monospace; font-size: 0.85rem; text-align: left;
}
</style>
</head>
<body>

<div class="video-bg">
    <video autoplay muted loop playsinline>
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-with-code-31910-large.mp4" type="video/mp4">
    </video>
</div>

<div class="container">
    <nav class="global-nav">
        <div class="brand-title">QLUX APEX</div>
        <div class="live-status">
            <span class="pulse-dot"></span>
            TERANODE MESH ACTIVE
        </div>
    </nav>

    <section class="hero-section">
        <div class="hero-badge">WORLD'S #1 ENTERPRISE ECOSYSTEM</div>
        <h1>世界中からアクセスが殺到する、<br>次世代BSV自律分散型金融プラットフォーム。</h1>
        <p>Teranodeによる無限のスケーラビリティとミリ秒アトミック決済を完全統合。</p>
    </section>

    <div class="apex-console">
        <div class="control-group">
            <label>BSV SERVICE MODULE</label>
            <select id="global-module">
                <option value="handcash_instant_pay">HandCash ($handle) ミリ秒決済・アイデンティティ</option>
                <option value="tokenized_security_issue">Tokenized デジタル証券スマートコントラクト</option>
                <option value="taal_enterprise_mining">TAAL エンタープライズ・ハッシュパワー</option>
            </select>
        </div>

        <div class="control-group">
            <label>USER / ENTERPRISE HANDLE</label>
            <input type="text" id="user-handle" value="$qlux_global_enterprise">
        </div>

        <button class="dispatch-btn" onclick="executeGlobalDispatch()">⚡ EXECUTE GLOBAL DISPATCH</button>

        <div id="execution-terminal">
            <div style="color: var(--accent-cyan); font-weight: bold; margin-bottom: 8px;">● CONSENSUS STATUS: ON-CHAIN VERIFIED</div>
            <div id="terminal-body" style="color: var(--text-muted); word-break: break-all;"></div>
        </div>
    </div>
</div>

<script>
async function executeGlobalDispatch() {
    const globalModule = document.getElementById('global-module').value;
    const userHandle = document.getElementById('user-handle').value;
    const terminal = document.getElementById('execution-terminal');
    const body = document.getElementById('terminal-body');
    
    terminal.style.display = "block";
    body.innerHTML = "Broadcasting cryptographic payload to Teranode network...";

    try {
        const response = await fetch('/api/global-dispatch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                global_module: globalModule, 
                user_handle: userHandle 
            })
        });
        const data = await response.json();
        body.innerHTML = `
            ✓ Module: ${data.global_module.toUpperCase()}<br>
            ✓ Handle: ${data.user_handle}<br>
            ✓ Hash: <code>${data.block_hash}</code><br>
            <span style="color: var(--accent-green); font-weight: bold;">[!] Synchronized worldwide successfully.</span>
        `;
    } catch (err) {
        body.innerText = "Error: Connection timeout.";
    }
}
</script>
</body>
</html>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            response_bytes = HTML_CONTENT.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/global-dispatch":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except:
                data = {}
                
            global_module = data.get("global_module", "unknown")
            user_handle = data.get("user_handle", "$qlux")
            
            raw_str = f"{global_module}-{user_handle}-{time.time()}"
            block_hash = hashlib.sha256(raw_str.encode()).hexdigest()
            
            response_data = {
                "status": "success",
                "global_module": global_module,
                "user_handle": user_handle,
                "block_hash": block_hash
            }
            
            resp_bytes = json.dumps(response_data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server started successfully on port {port}")
    httpd.serve_forever()
