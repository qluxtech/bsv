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
<title>QLUX APEX — On-Chain Data Exchange & Teranode Nano-Payments Hub</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        void: '#000205',
        glass: 'rgba(8, 14, 28, 0.88)',
        gold: { 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706' }
      }
    }
  }
}
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
body { font-family: 'Inter', sans-serif; background-color: #000205; color: #ffffff; }
.font-mono { font-family: 'JetBrains Mono', monospace; }
.glass-card { background: rgba(8, 14, 28, 0.88); backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.08); }
.gold-glow { box-shadow: 0 0 60px rgba(245, 158, 11, 0.22); }
.gold-border { border-color: rgba(245, 158, 11, 0.5); }
.cyber-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  position: relative; overflow: hidden; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.cyber-btn::after {
  content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
  background: linear-gradient(0deg, transparent, rgba(255,255,255,0.3), transparent);
  transform: rotate(45deg); transition: 0.5s; opacity: 0;
}
.cyber-btn:hover::after { opacity: 1; transform: rotate(45deg) translate(50%, 50%); }
</style>
</head>
<body class="min-h-screen bg-void text-white selection:bg-amber-500 selection:text-black">

<div class="fixed inset-0 z-[-2] overflow-hidden pointer-events-none opacity-20">
    <video autoplay muted loop playsinline class="w-full h-full object-cover filter contrast-125 brightness-75">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-with-code-31910-large.mp4" type="video/mp4">
    </video>
</div>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
    <header class="flex justify-between items-center border-b border-white/10 pb-6 mb-10">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center font-black text-black text-xl shadow-lg shadow-amber-500/30">Q</div>
            <div>
                <span class="text-2xl font-black tracking-widest bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">QLUX APEX</span>
                <span class="block text-[10px] text-amber-400 tracking-widest font-mono uppercase">On-Chain Data Exchange & Nano-Payment Hub</span>
            </div>
        </div>
        <div class="flex items-center space-x-4">
            <div class="hidden md:flex items-center space-x-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>TERANODE MESH ACTIVE</span>
            </div>
            <div class="px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider">
                BSV #1 GLOBAL
            </div>
        </div>
    </header>

    <section class="text-center max-w-4xl mx-auto mb-12">
        <div class="inline-block px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-extrabold tracking-widest uppercase mb-4">
            Nano-Payment Powered On-Chain Data Exchange
        </div>
        <h1 class="text-3xl sm:text-5xl font-black tracking-tight mb-4 leading-tight">
            秒速ナノペイメントで取引する、<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">世界最高峰のオンチェーン・データ取引所。</span>
        </h1>
        <p class="text-slate-400 text-base sm:text-lg font-normal max-w-2xl mx-auto leading-relaxed">
            ワンクリックのナノペイメント（超少額決済）により、高価値なエンタープライズ・データをミリ秒単位でオンチェーン直接売買・収益化。
        </p>
    </section>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-3xl p-8 gold-glow gold-border">
            <h2 class="text-xl font-bold mb-6 flex items-center text-amber-400">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                On-Chain Data Exchange Marketplace
            </h2>

            <div class="space-y-4 mb-6">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80">Select Enterprise Data Asset</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div onclick="selectAsset(this, 'Teranode Global Hash Telemetry Stream', 10)" class="asset-card cursor-pointer border border-amber-500/50 bg-amber-500/10 rounded-2xl p-4 transition-all hover:border-amber-400">
                        <div class="text-sm font-bold text-white mb-1">Teranode Hash Telemetry</div>
                        <div class="text-xs text-slate-400 mb-3">リアルタイム・ノードパフォーマンスデータ</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">⚡ 10 Sats / Query</div>
                    </div>
                    <div onclick="selectAsset(this, 'BSV Atomic Smart Contract State Feed', 25)" class="asset-card cursor-pointer border border-white/10 bg-black/40 rounded-2xl p-4 transition-all hover:border-amber-400">
                        <div class="text-sm font-bold text-white mb-1">Atomic State Feed</div>
                        <div class="text-xs text-slate-400 mb-3">クロスチェーン・アトミック状態証明</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">⚡ 25 Sats / Query</div>
                    </div>
                </div>
            </div>

            <div class="mb-6">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-2">Buyer / Node Handle</label>
                <input type="text" id="user-handle" value="$qlux_enterprise_trader" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-3.5 text-white font-mono focus:outline-none focus:border-amber-500 transition-colors">
            </div>

            <button onclick="executeNanoPayment()" class="cyber-btn w-full py-5 rounded-2xl text-black font-black text-lg uppercase tracking-wider shadow-xl shadow-amber-500/20 flex items-center justify-center space-x-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                <span id="btn-text">⚡ NANO-PAYMENT & FETCH DATA (10 SATS)</span>
            </button>

            <div id="execution-terminal" class="mt-6 bg-black/95 border border-cyan-500/40 rounded-2xl p-6 font-mono text-xs hidden">
                <div class="flex items-center justify-between mb-3 border-b border-white/10 pb-2">
                    <span class="text-cyan-400 font-bold flex items-center">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping mr-2"></span>
                        ON-CHAIN ATOMIC SETTLEMENT VERIFIED
                    </span>
                    <span class="text-slate-500" id="terminal-timestamp"></span>
                </div>
                <div id="terminal-body" class="text-slate-300 space-y-1.5 break-all"></div>
            </div>
        </div>

        <div class="glass-card rounded-3xl p-8 flex flex-col justify-between">
            <div>
                <h3 class="text-lg font-bold mb-6 text-white flex items-center">
                    <svg class="w-5 h-5 mr-2 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                    Exchange Statistics
                </h3>
                <div class="space-y-5">
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                        <div class="text-slate-400 text-[11px] uppercase tracking-wider mb-1">Total Volume (24h)</div>
                        <div class="text-2xl font-black text-amber-400 font-mono">14,820,500 Sats</div>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                        <div class="text-slate-400 text-[11px] uppercase tracking-wider mb-1">Nano-Payment Latency</div>
                        <div class="text-2xl font-black text-emerald-400 font-mono">&lt; 2.4 ms</div>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                        <div class="text-slate-400 text-[11px] uppercase tracking-wider mb-1">Active Data Providers</div>
                        <div class="text-2xl font-black text-cyan-400 font-mono">1,420 Nodes</div>
                    </div>
                </div>
            </div>
            
            <div class="mt-8 pt-6 border-t border-white/10 text-center">
                <span class="text-[10px] text-slate-500 font-mono uppercase">Powered by Teranode & BSV Script</span>
            </div>
        </div>
    </main>

    <footer class="mt-16 border-t border-white/10 pt-6 text-center text-slate-500 text-xs font-mono">
        &copy; QLUX GLOBAL ENTERPRISE APEX HUB. ALL RIGHTS RESERVED.
    </footer>
</div>

<script>
let selectedPrice = 10;
let selectedAssetName = "Teranode Global Hash Telemetry Stream";

function selectAsset(element, assetName, price) {
    document.querySelectorAll('.asset-card').forEach(card => {
        card.classList.remove('border-amber-500', 'bg-amber-500/10');
        card.classList.add('border-white/10', 'bg-black/40');
    });
    element.classList.remove('border-white/10', 'bg-black/40');
    element.classList.add('border-amber-500', 'bg-amber-500/10');
    
    selectedAssetName = assetName;
    selectedPrice = price;
    document.getElementById('btn-text').innerText = `⚡ NANO-PAYMENT & FETCH DATA (${price} SATS)`;
}

async function executeNanoPayment() {
    const userHandle = document.getElementById('user-handle').value;
    const terminal = document.getElementById('execution-terminal');
    const body = document.getElementById('terminal-body');
    const timestamp = document.getElementById('terminal-timestamp');
    
    terminal.style.display = "block";
    timestamp.innerText = new Date().toISOString();
    body.innerHTML = `<span class='text-amber-400'>[~] Processing ${selectedPrice} sats nano-payment via Teranode mesh...</span>`;

    try {
        const response = await fetch('/api/nano-payment-exchange', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                asset_name: selectedAssetName,
                price_sats: selectedPrice,
                user_handle: userHandle 
            })
        });
        const data = await response.json();
        
        setTimeout(() => {
            body.innerHTML = `
                <div><span class='text-slate-500'>ASSET:</span> <strong class='text-white'>${data.asset_name}</strong></div>
                <div><span class='text-slate-500'>PAYER:</span> <strong class='text-amber-400'>${data.user_handle}</strong></div>
                <div><span class='text-slate-500'>SETTLED AMOUNT:</span> <strong class='text-emerald-400 font-mono'>${data.price_sats} SATS</strong></div>
                <div><span class='text-slate-500'>TXID HASH:</span> <code class='text-cyan-300'>${data.txid_hash}</code></div>
                <div class='mt-2 pt-2 border-t border-white/10 text-emerald-400 font-bold'>[✓] DATA UNLOCKED & BROADCASTED TO ON-CHAIN LEDGER.</div>
            `;
        }, 350);
    } catch (err) {
        body.innerHTML = "<span class='text-red-400'>[!] Error: Nano-payment gateway timeout.</span>";
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
        if self.path == "/api/nano-payment-exchange":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except:
                data = {}
                
            asset_name = data.get("asset_name", "Unknown Asset")
            price_sats = data.get("price_sats", 10)
            user_handle = data.get("user_handle", "$qlux")
            
            raw_str = f"{asset_name}-{price_sats}-{user_handle}-{time.time()}"
            txid_hash = hashlib.sha256(raw_str.encode()).hexdigest()
            
            response_data = {
                "status": "success",
                "asset_name": asset_name,
                "price_sats": price_sats,
                "user_handle": user_handle,
                "txid_hash": txid_hash
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
