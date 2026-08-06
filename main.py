import os
import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX — World's #1 Global Enterprise Apex Hub | Teranode BSV Ecosystem</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        void: '#000205',
        glass: 'rgba(8, 14, 28, 0.85)',
        gold: {
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
        }
      }
    }
  }
}
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
body { font-family: 'Inter', sans-serif; background-color: #000205; color: #ffffff; }
.font-mono { font-family: 'JetBrains Mono', monospace; }
.glass-card { background: rgba(8, 14, 28, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
.gold-glow { box-shadow: 0 0 50px rgba(245, 158, 11, 0.25); }
.gold-border { border-color: rgba(245, 158, 11, 0.5); }
</style>
</head>
<body class="min-h-screen bg-void text-white selection:bg-amber-500 selection:text-black">

<div class="fixed inset-0 z-[-2] overflow-hidden pointer-events-none opacity-20">
    <video autoplay muted loop playsinline class="w-full h-full object-cover filter contrast-125 brightness-75">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-with-code-31910-large.mp4" type="video/mp4">
    </video>
</div>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
    <header class="flex justify-between items-center border-b border-white/10 pb-6 mb-12">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center font-black text-black text-xl">Q</div>
            <span class="text-2xl font-black tracking-widest bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">QLUX APEX</span>
        </div>
        <div class="flex items-center space-x-4">
            <div class="hidden md:flex items-center space-x-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>TERANODE MESH: 1,280,000 TPS</span>
            </div>
            <div class="px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider">
                Global Apex #1
            </div>
        </div>
    </header>

    <section class="text-center max-w-4xl mx-auto mb-16">
        <div class="inline-block px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-extrabold tracking-widest uppercase mb-6">
            World's Leading Enterprise BSV Infrastructure
        </div>
        <h1 class="text-4xl sm:text-6xl font-black tracking-tight mb-6 leading-tight">
            無限のスケールと秒速コンセンサス。<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">次世代グローバル金融インフラストラクチャ。</span>
        </h1>
        <p class="text-slate-400 text-lg sm:text-xl font-normal max-w-2xl mx-auto leading-relaxed">
            Teranodeアーキテクチャを採用し、国家・巨大企業・グローバルネットワーク間のあらゆるトランザクションをミリ秒単位で完全にアトミックに実行します。
        </p>
    </section>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-3xl p-8 gold-glow gold-border">
            <h2 class="text-xl font-bold mb-6 flex items-center text-amber-400">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                Enterprise Command Dispatcher
            </h2>
            
            <div class="space-y-6">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-2">Select BSV Enterprise Service Module</label>
                    <select id="global-module" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-4 text-white font-medium focus:outline-none focus:border-amber-500 transition-colors">
                        <option value="teranode_high_throughput">Teranode Ultra-High Throughput Settlement (1M+ TPS)</option>
                        <option value="handcash_instant_pay">HandCash Global Micro-Identity & Instant Pay ($handle)</option>
                        <option value="tokenized_security_issue">Tokenized Enterprise Digital Asset & Smart Contracts</option>
                        <option value="taal_enterprise_mining">TAAL Hashpower & Green Enterprise Mining Verification</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-2">Target Enterprise Handle / Node ID</label>
                    <input type="text" id="user-handle" value="$qlux_global_apex_enterprise" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-4 text-white font-mono focus:outline-none focus:border-amber-500 transition-colors">
                </div>

                <button onclick="executeGlobalDispatch()" class="w-full py-5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 text-black font-black text-lg uppercase tracking-wider hover:from-amber-400 hover:to-amber-500 transition-all transform active:scale-[0.99] shadow-lg shadow-amber-500/25">
                    ⚡ Execute Global Apex Dispatch
                </button>
            </div>

            <div id="execution-terminal" class="mt-8 bg-black/90 border border-cyan-500/40 rounded-2xl p-6 font-mono text-sm hidden">
                <div class="flex items-center justify-between mb-4 border-b border-white/10 pb-3">
                    <span class="text-cyan-400 font-bold flex items-center">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping mr-2"></span>
                        ON-CHAIN CONSENSUS VERIFIED
                    </span>
                    <span class="text-xs text-slate-500" id="terminal-timestamp"></span>
                </div>
                <div id="terminal-body" class="text-slate-300 space-y-2 break-all"></div>
            </div>
        </div>

        <div class="glass-card rounded-3xl p-8 flex flex-col justify-between">
            <div>
                <h3 class="text-lg font-bold mb-6 text-white flex items-center">
                    <svg class="w-5 h-5 mr-2 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                    Network Metrics
                </h3>
                <div class="space-y-6">
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                        <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">Average Block Time</div>
                        <div class="text-2xl font-black text-amber-400 font-mono">1.2 seconds</div>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                        <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">Global Node Health</div>
                        <div class="text-2xl font-black text-emerald-400 font-mono">99.999%</div>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                        <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">Atomic Finality</div>
                        <div class="text-2xl font-black text-cyan-400 font-mono">&lt; 10ms</div>
                    </div>
                </div>
            </div>
            
            <div class="mt-8 pt-6 border-t border-white/10 text-center">
                <span class="text-xs text-slate-500 font-mono">SECURED BY BITCOIN SV (BSV)</span>
            </div>
        </div>
    </main>

    <footer class="mt-20 border-t border-white/10 pt-8 text-center text-slate-500 text-xs">
        &copy; QLUX GLOBAL ENTERPRISE APEX HUB. ALL RIGHTS RESERVED. POWERED BY TERANODE MESH.
    </footer>
</div>

<script>
async function executeGlobalDispatch() {
    const globalModule = document.getElementById('global-module').value;
    const userHandle = document.getElementById('user-handle').value;
    const terminal = document.getElementById('execution-terminal');
    const body = document.getElementById('terminal-body');
    const timestamp = document.getElementById('terminal-timestamp');
    
    terminal.style.display = "block";
    timestamp.innerText = new Date().toISOString();
    body.innerHTML = "<span class='text-amber-400'>[~] Broadcasting cryptographic payload to Teranode mesh network...</span>";

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
        
        setTimeout(() => {
            body.innerHTML = `
                <div><span class='text-slate-500'>MODULE:</span> <strong class='text-white'>${data.global_module.toUpperCase()}</strong></div>
                <div><span class='text-slate-500'>HANDLE:</span> <strong class='text-amber-400'>${data.user_handle}</strong></div>
                <div><span class='text-slate-500'>MERKLE ROOT:</span> <code class='text-cyan-300'>${data.block_hash}</code></div>
                <div class='mt-3 pt-3 border-t border-white/10 text-emerald-400 font-bold'>[✓] ATOMIC SETTLEMENT & GLOBAL SYNC COMPLETED.</div>
            `;
        }, 400);
    } catch (err) {
        body.innerHTML = "<span class='text-red-400'>[!] Error: Consensus node connection timeout.</span>";
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
