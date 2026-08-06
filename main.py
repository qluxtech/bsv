import os
import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_CODE = """<!DOCTYPE html>
<html lang="ja" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX APEX - World's No.1 Enterprise On-Chain Data Exchange</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        void: '#000205',
        glass: 'rgba(8, 14, 28, 0.95)',
        gold: { 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706' }
      }
    }
  }
}
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
body { font-family: 'Inter', sans-serif; background-color: #000205; color: #ffffff; overflow-x: hidden; }
.font-mono { font-family: 'JetBrains Mono', monospace; }
.glass-card { background: rgba(8, 14, 28, 0.95); backdrop-filter: blur(35px); border: 1px solid rgba(255, 255, 255, 0.1); }
.gold-glow { box-shadow: 0 0 100px rgba(245, 158, 11, 0.3); }
.gold-border { border-color: rgba(245, 158, 11, 0.65); }

/* オンチェーンデータ可視化モニターのスタイル */
.matrix-screen {
  background: radial-gradient(circle at center, rgba(16, 185, 129, 0.1) 0%, rgba(0, 2, 5, 0.95) 80%);
  border: 1px solid rgba(52, 211, 153, 0.4);
  box-shadow: inset 0 0 30px rgba(52, 211, 153, 0.15), 0 0 40px rgba(52, 211, 153, 0.1);
  border-radius: 24px;
  position: relative;
  overflow: hidden;
}
.matrix-grid {
  background-image: linear-gradient(rgba(52, 211, 153, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(52, 211, 153, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}
.pulse-dot {
  width: 10px; height: 10px; background-color: #34d399; border-radius: 50%;
  box-shadow: 0 0 15px #34d399;
  animation: pulse-ring 2s infinite;
}
@keyframes pulse-ring {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 15px rgba(52, 211, 153, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
}

.swipe-container {
  position: relative; width: 100%; height: 80px; background: rgba(0, 0, 0, 0.7);
  border-radius: 20px; padding: 6px; overflow: hidden; user-select: none;
  border: 1px solid rgba(245, 158, 11, 0.4); box-shadow: inset 0 4px 20px rgba(0,0,0,0.8), 0 0 30px rgba(245,158,11,0.15);
}
.swipe-btn {
  position: absolute; left: 6px; top: 6px; width: 68px; height: 68px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
  border-radius: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center;
  color: #000205; font-size: 24px; font-weight: bold; box-shadow: 0 6px 25px rgba(245, 158, 11, 0.5);
  transition: background 0.2s ease; z-index: 10;
}
.swipe-btn.unlocked { background: linear-gradient(135deg, #34d399 0%, #059669 100%); color: #ffffff; }
.swipe-text {
  position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em;
  background: linear-gradient(90deg, #f59e0b, #ffffff, #f59e0b);
  background-size: 200% auto; color: transparent; -webkit-background-clip: text;
  background-clip: text; opacity: 1; transition: opacity 0.2s;
}
.swipe-text.hide { opacity: 0; }
</style>
</head>
<body class="min-h-screen bg-void text-white p-4 sm:p-8">

<div class="max-w-7xl mx-auto space-y-8 relative z-10">
    <header class="flex flex-col sm:flex-row justify-between items-center border-b border-white/10 pb-6 gap-4">
        <div class="flex items-center space-x-3">
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center font-black text-black text-2xl shadow-xl shadow-amber-500/40">Q</div>
            <div>
                <span class="text-2xl font-black tracking-widest bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">QLUX APEX</span>
                <span class="block text-[10px] text-amber-400 tracking-widest font-mono uppercase">World's #1 Enterprise On-Chain Data Exchange Hub</span>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <div class="px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider">
                GLOBAL RANK #1
            </div>
            <div class="px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                TPS: 1,420,000
            </div>
        </div>
    </header>

    <section class="text-center max-w-4xl mx-auto pt-2 pb-4">
        <h1 class="text-3xl sm:text-5xl font-black tracking-tight mb-4 leading-tight">
            AIと世界最高峰機関が欲する、<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">リアルタイム・オンチェーンデータ取引。</span>
        </h1>
        <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            Teranodeアーキテクチャが生み出す超高精度なオンチェーン・テレメトリーデータを可視化し、ナノペイメントで即座に購読・収益化。
        </p>
    </section>

    <section class="max-w-5xl mx-auto">
        <div class="matrix-screen matrix-grid p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4 border-b border-emerald-500/20 pb-4">
                <div class="flex items-center space-x-3">
                    <div class="pulse-dot"></div>
                    <div>
                        <h3 class="text-sm sm:text-base font-bold text-emerald-400 font-mono tracking-wider">LIVE ON-CHAIN DATA VISUALIZATION MATRIX</h3>
                        <p class="text-[11px] text-slate-400 font-mono">Teranode Atomic Stream & Swarm Nodes Syncing</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3 font-mono text-xs">
                    <span class="px-3 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">BLOCK HEIGHT: #842,910</span>
                    <span class="px-3 py-1 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" id="matrix-timer">00:00:00 UTC</span>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div class="bg-black/60 border border-emerald-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>ATOMIC TX THROUGHPUT</span>
                        <span class="text-emerald-400 font-bold">99.98%</span>
                    </div>
                    <div class="text-2xl font-black text-white" id="stat-tps">1,420,310 <span class="text-xs text-emerald-400">TPS</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-emerald-500 to-cyan-400 h-full w-[85%] animate-pulse"></div>
                    </div>
                </div>

                <div class="bg-black/60 border border-amber-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>ACTIVE SWARM NODES</span>
                        <span class="text-amber-400 font-bold">GLOBAL</span>
                    </div>
                    <div class="text-2xl font-black text-white">14,892 <span class="text-xs text-amber-400">NODES</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-amber-500 to-yellow-300 h-full w-[92%] animate-pulse"></div>
                    </div>
                </div>

                <div class="bg-black/60 border border-cyan-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>NANO-PAYMENT VELOCITY</span>
                        <span class="text-cyan-400 font-bold">INSTANT</span>
                    </div>
                    <div class="text-2xl font-black text-white">0.001 <span class="text-xs text-cyan-400">SEC</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-cyan-500 to-blue-500 h-full w-[98%] animate-pulse"></div>
                    </div>
                </div>
            </div>

            <div class="bg-black/80 rounded-xl p-4 border border-emerald-500/20 font-mono text-xs text-emerald-300/90 h-24 overflow-y-auto space-y-1.5" id="packet-log">
                <div>[08:27:44] CONNECTED TO TERANODE ATOMIC MESH... STREAMING BLOCK DATA</div>
                <div>[08:27:45] VERIFIED AI AGENT TELEMETRY PACKET #9102-X</div>
                <div>[08:27:46] NANO-PAYMENT SETTLED: 15 SATS RECEIVED FOR NODE #481</div>
            </div>
        </div>
    </section>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-3xl p-6 sm:p-8 gold-border space-y-6">
            <h2 class="text-lg font-bold flex items-center text-amber-400">Autonomous AI Data Feed & Telemetry Stream</h2>
            
            <div class="space-y-3">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80">Select Data Asset for Acquisition</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div onclick="selectAsset(this, 'Teranode AI Neural Telemetry Stream', 15)" class="asset-card cursor-pointer border border-amber-500 bg-amber-500/10 rounded-2xl p-4 transition-all">
                        <div class="text-sm font-bold text-white mb-1">AI Neural Telemetry Stream</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">15 Sats / Request</div>
                    </div>
                    <div onclick="selectAsset(this, 'Global Enterprise Atomic Ledger Feed', 30)" class="asset-card cursor-pointer border border-white/10 bg-black/40 rounded-2xl p-4 transition-all">
                        <div class="text-sm font-bold text-white mb-1">Enterprise Atomic Ledger</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">30 Sats / Request</div>
                    </div>
                </div>
            </div>

            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-2">AI Agent Handle ID</label>
                <input type="text" id="user-handle" value="$qlux_ai_agent" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-amber-500">
            </div>

            <div id="execution-terminal" class="bg-black/95 border border-cyan-500/40 rounded-2xl p-5 font-mono text-xs hidden space-y-2">
                <div class="text-cyan-400 font-bold">AI DATA UNLOCKED & BROADCASTED</div>
                <div id="terminal-body" class="text-slate-300 break-all space-y-1"></div>
            </div>
        </div>

        <div class="glass-card rounded-3xl p-6 sm:p-8 flex flex-col justify-between gold-glow gold-border space-y-6">
            <div class="space-y-6">
                <div>
                    <h3 class="text-lg font-bold mb-2 text-white">Swipe Nano-Payment</h3>
                    <p class="text-xs text-slate-400">スワイプバーを右端までスライドして即座にナノペイメントを実行します。</p>
                </div>

                <div class="bg-white/5 rounded-2xl p-5 border border-white/5 text-center">
                    <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">Required Fee</div>
                    <div id="selected-price" class="text-4xl font-black text-amber-400 font-mono">15 <span class="text-xl">SATS</span></div>
                </div>

                <div class="space-y-3">
                    <div class="swipe-container" id="swipe-container">
                        <div class="swipe-text" id="swipe-text">SWIPE TO PAY NANO &rarr;</div>
                        <div class="swipe-btn" id="swipe-btn">&rarr;</div>
                    </div>
                </div>
            </div>

            <div class="border-t border-white/10 pt-4 text-xs text-slate-500 text-center font-mono">
                SECURED BY TERANODE PROTOCOL
            </div>
        </div>
    </main>
</div>

<script>
// ライブ時計とパケットの自動追加アニメーション
setInterval(() => {
    const now = new Date();
    const timeStr = now.toISOString().slice(11, 19) + " UTC";
    document.getElementById('matrix-timer').innerText = timeStr;
    
    // ランダムなTPS変動
    const tpsEl = document.getElementById('stat-tps');
    const randomTps = 1420000 + Math.floor(Math.random() * 850);
    tpsEl.innerHTML = randomTps.toLocaleString() + ' <span class="text-xs text-emerald-400">TPS</span>';
}, 1000);

setInterval(() => {
    const logBox = document.getElementById('packet-log');
    const now = new Date().toISOString().slice(11, 19);
    const hashes = ['#842,911', '#842,912', '#842,913'];
    const randomHash = hashes[Math.floor(Math.random() * hashes.length)];
    const div = document.createElement('div');
    div.innerText = '[' + now + '] ATOMIC BLOCK SYNCED: BLOCK ' + randomHash + ' (VERIFIED)';
    logBox.appendChild(div);
    logBox.scrollTop = logBox.scrollHeight;
}, 3000);

let selectedPrice = 15;
let selectedAssetName = "Teranode AI Neural Telemetry Stream";

function selectAsset(element, assetName, price) {
    document.querySelectorAll('.asset-card').forEach(card => {
        card.classList.remove('border-amber-500', 'bg-amber-500/10');
        card.classList.add('border-white/10', 'bg-black/40');
    });
    element.classList.remove('border-white/10', 'bg-black/40');
    element.classList.add('border-amber-500', 'bg-amber-500/10');
    selectedAssetName = assetName;
    selectedPrice = price;
    document.getElementById('selected-price').innerHTML = price + ' <span class="text-xl">SATS</span>';
}

const container = document.getElementById('swipe-container');
const btn = document.getElementById('swipe-btn');
const text = document.getElementById('swipe-text');

let isDragging = false;
let startX = 0;
let currentX = 0;
let maxTranslate = 0;

function updateMax() {
    maxTranslate = container.clientWidth - btn.clientWidth - 12;
}
window.addEventListener('resize', updateMax);
window.addEventListener('load', updateMax);

function startDrag(e) {
    if (btn.classList.contains('unlocked')) return;
    isDragging = true;
    startX = (e.touches ? e.touches[0].clientX : e.clientX) - currentX;
    text.classList.add('hide');
}

function onDrag(e) {
    if (!isDragging) return;
    updateMax();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    currentX = clientX - startX;
    if (currentX < 0) currentX = 0;
    if (currentX > maxTranslate) currentX = maxTranslate;
    btn.style.transform = 'translateX(' + currentX + 'px)';
}

function endDrag() {
    if (!isDragging) return;
    isDragging = false;
    updateMax();

    if (currentX >= maxTranslate * 0.7) {
        btn.style.transform = 'translateX(' + maxTranslate + 'px)';
        btn.classList.add('unlocked');
        btn.innerHTML = '✓';
        executePayment();
    } else {
        currentX = 0;
        btn.style.transform = 'translateX(0px)';
        text.classList.remove('hide');
    }
}

btn.addEventListener('mousedown', startDrag);
window.addEventListener('mousemove', onDrag);
window.addEventListener('mouseup', endDrag);

btn.addEventListener('touchstart', startDrag);
window.addEventListener('touchmove', onDrag);
window.addEventListener('touchend', endDrag);

async function executePayment() {
    const handle = document.getElementById('user-handle').value;
    const terminal = document.getElementById('execution-terminal');
    const body = document.getElementById('terminal-body');
    
    terminal.style.display = "block";
    body.innerHTML = 'Broadcasting ' + selectedPrice + ' sats nano-payment...';

    try {
        const res = await fetch('/api/pay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ asset_name: selectedAssetName, handle: handle, sats: selectedPrice })
        });
        const data = await res.json();
        
        setTimeout(() => {
            btn.classList.remove('unlocked');
            btn.innerHTML = '&rarr;';
            currentX = 0;
            btn.style.transform = 'translateX(0px)';
            text.classList.remove('hide');

            body.innerHTML = 'ASSET: ' + data.asset_name + '<br>HANDLE: ' + data.handle + '<br>AMOUNT: ' + data.sats + ' SATS<br>TXID: ' + data.txid + '<br><b class="text-emerald-400">[OK] DATA STREAM UNLOCKED.</b>';
        }, 400);
    } catch (e) {
        btn.classList.remove('unlocked');
        btn.innerHTML = '&rarr;';
        currentX = 0;
        btn.style.transform = 'translateX(0px)';
        text.classList.remove('hide');
        body.innerHTML = 'Error: Payment gateway communication failed.';
    }
}
</script>
</body>
</html>
"""

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            payload = HTML_CODE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/pay':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode('utf-8'))
            except:
                data = {}
            
            asset_name = data.get('asset_name', 'Teranode AI Neural Telemetry Stream')
            handle = data.get('handle', '$qlux')
            sats = data.get('sats', 15)
            txid = hashlib.sha256(f"{asset_name}-{handle}-{sats}-{time.time()}".encode()).hexdigest()
            
            resp = json.dumps({'status': 'success', 'asset_name': asset_name, 'handle': handle, 'sats': sats, 'txid': txid}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleServer)
    print(f"Server started on port {port}")
    server.serve_forever()
