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
<title>QLUX APEX — World's #1 Enterprise On-Chain Data Exchange & Nano-Payments</title>
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

/* 超高級・究極スワイプボタンのスタイル */
.swipe-container {
  position: relative; width: 100%; height: 84px; background: rgba(0, 0, 0, 0.6);
  border-radius: 24px; padding: 6px; overflow: hidden; user-select: none;
  border: 1px solid rgba(245, 158, 11, 0.3); box-shadow: inset 0 4px 20px rgba(0,0,0,0.8), 0 0 30px rgba(245,158,11,0.1);
}
.swipe-btn {
  position: absolute; left: 6px; top: 6px; width: 72px; height: 72px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
  border-radius: 18px; cursor: grab; display: flex; align-items: center; justify-content: center;
  color: #000205; box-shadow: 0 6px 25px rgba(245, 158, 11, 0.5);
  transition: background 0.3s ease, box-shadow 0.3s ease;
  z-index: 10;
}
.swipe-btn:active { cursor: grabbing; }
.swipe-btn.unlocked { background: linear-gradient(135deg, #34d399 0%, #059669 100%); color: #ffffff; box-shadow: 0 0 35px rgba(52, 211, 153, 0.8); }
.swipe-btn.processing { background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%); color: #ffffff; cursor: wait; box-shadow: 0 0 35px rgba(56, 189, 248, 0.8); }

.swipe-text {
  position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em;
  background: linear-gradient(90deg, #f59e0b, #ffffff, #f59e0b);
  background-size: 200% auto; color: transparent; -webkit-background-clip: text;
  background-clip: text; animation: shine 2.5s linear infinite; opacity: 1; transition: opacity 0.3s;
}
.swipe-text.hide { opacity: 0; }

.security-ring {
  position: absolute; top: -6px; left: -6px; width: 84px; height: 84px;
  border: 2px solid transparent; border-top-color: #fbbf24; border-right-color: #38bdf8; border-radius: 22px;
  opacity: 0; pointer-events: none;
}
.swipe-btn.sliding .security-ring { opacity: 1; animation: spin 0.8s linear infinite; }

@keyframes shine { to { background-position: 200% center; } }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>
</head>
<body class="min-h-screen bg-void text-white selection:bg-amber-500 selection:text-black">

<div class="fixed inset-0 z-[-2] overflow-hidden pointer-events-none opacity-20">
    <video autoplay muted loop playsinline class="w-full h-full object-cover filter contrast-125 brightness-75">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-with-code-31910-large.mp4" type="video/mp4">
    </video>
</div>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
    <header class="flex justify-between items-center border-b border-white/10 pb-5 mb-8">
        <div class="flex items-center space-x-3">
            <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center font-black text-black text-xl shadow-xl shadow-amber-500/40">Q</div>
            <div>
                <span class="text-2xl font-black tracking-widest bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">QLUX APEX</span>
                <span class="block text-[10px] text-amber-400 tracking-widest font-mono uppercase">World's #1 Enterprise On-Chain Data Exchange Hub</span>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <div class="hidden md:flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[11px] font-bold">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>TERANODE AI STREAM ACTIVE</span>
            </div>
            <div class="px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[11px] font-bold uppercase tracking-wider">
                GLOBAL RANK #1
            </div>
        </div>
    </header>

    <section class="text-center max-w-4xl mx-auto mb-10">
        <div class="inline-block px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[10px] font-extrabold tracking-widest uppercase mb-3">
            Autonomous AI & Enterprise Data Intelligence
        </div>
        <h1 class="text-3xl sm:text-5xl font-black tracking-tight mb-3 leading-tight">
            AIと世界最高峰機関が欲する、<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">リアルタイム・オンチェーンデータ取引。</span>
        </h1>
        <p class="text-slate-400 text-sm sm:text-base font-normal max-w-2xl mx-auto leading-relaxed">
            Teranodeアーキテクチャが生み出す超高精度なオンチェーン・テレメトリーデータを可視化し、ナノペイメントで即座に購読・収益化。
        </p>
    </section>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-3xl p-7 gold-border">
            <h2 class="text-lg font-bold mb-4 flex items-center text-amber-400">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                Autonomous AI Data Feed & Telemetry Stream
            </h2>
            <p class="text-xs text-slate-400 mb-5">AIエージェントおよびグローバル金融機関がAPI経由でリアルタイムに常時吸い上げる高価値データストリーム。</p>

            <div class="bg-black/80 border border-cyan-500/30 rounded-2xl p-5 mb-6 font-mono text-xs">
                <div class="flex justify-between items-center mb-3 border-b border-white/10 pb-2">
                    <span class="text-cyan-400 font-bold flex items-center">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping mr-2"></span>
                        LIVE STREAM: TERANODE_AI_TELEMETRY_v4
                    </span>
                    <span class="text-slate-500" id="live-clock">00:00:00 UTC</span>
                </div>
                <div class="space-y-2 text-slate-300">
                    <div class="flex justify-between bg-white/5 p-2 rounded-xl">
                        <span class="text-slate-400">Active AI Swarm Consumers:</span>
                        <span class="text-amber-400 font-bold">14,892 Nodes</span>
                    </div>
                    <div class="flex justify-between bg-white/5 p-2 rounded-xl">
                        <span class="text-slate-400">Instant Throughput Velocity:</span>
                        <span class="text-emerald-400 font-bold">1,420,000 TPS</span>
                    </div>
                    <div class="flex justify-between bg-white/5 p-2 rounded-xl">
                        <span class="text-slate-400">Merkle Root Hash State:</span>
                        <span class="text-cyan-300 truncate max-w-[220px]" id="live-merkle">0x9f8b...31a2c7</span>
                    </div>
                </div>
            </div>

            <div class="space-y-3 mb-5">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80">Select Data Asset for Acquisition</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div onclick="selectAsset(this, 'Teranode AI Neural Telemetry Stream', 15)" class="asset-card cursor-pointer border border-amber-500/50 bg-amber-500/10 rounded-2xl p-3.5 transition-all hover:border-amber-400">
                        <div class="text-sm font-bold text-white mb-0.5">AI Neural Telemetry Stream</div>
                        <div class="text-xs text-slate-400 mb-2">AIモデル最適化学習用オンチェーンデータ</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">⚡ 15 Sats / Request</div>
                    </div>
                    <div onclick="selectAsset(this, 'Global Enterprise Atomic Ledger Feed', 30)" class="asset-card cursor-pointer border border-white/10 bg-black/40 rounded-2xl p-3.5 transition-all hover:border-amber-400">
                        <div class="text-sm font-bold text-white mb-0.5">Enterprise Atomic Ledger</div>
                        <div class="text-xs text-slate-400 mb-2">金融機関向けリアルタイム取引検証データ</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">⚡ 30 Sats / Request</div>
                    </div>
                </div>
            </div>

            <div class="mb-2">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-1.5">AI Agent / Buyer Handle ID</label>
                <input type="text" id="user-handle" value="$qlux_autonomous_ai_agent" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-amber-500 transition-colors">
            </div>

            <div id="execution-terminal" class="mt-5 bg-black/95 border border-cyan-500/40 rounded-2xl p-5 font-mono text-xs hidden">
                <div class="flex items-center justify-between mb-3 border-b border-white/10 pb-2">
                    <span class="text-cyan-400 font-bold flex items-center">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping mr-2"></span>
                        AI DATA UNLOCKED & BROADCASTED
                    </span>
                    <span class="text-slate-500" id="terminal-timestamp"></span>
                </div>
                <div id="terminal-body" class="text-slate-300 space-y-1.5 break-all"></div>
            </div>
        </div>

        <div class="glass-card rounded-3xl p-7 flex flex-col justify-between gold-glow gold-border">
            <div>
                <h3 class="text-lg font-bold mb-4 text-white flex items-center">
                    <svg class="w-5 h-5 mr-2 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    Swipe Nano-Payment
                </h3>
                <p class="text-xs text-slate-400 mb-5">スワイプするだけで一瞬でオンチェーン決済が完了し、高価値データが即座にアンロックされます。</p>
                
                <div class="bg-white/5 rounded-2xl p-4 border border-white/5 mb-6 text-center shadow-inner">
                    <div class="text-slate-400 text-[11px] uppercase tracking-wider mb-0.5">Required Nano-Payment Fee</div>
                    <div id="selected-price" class="text-4xl font-black text-amber-400 font-mono">15 <span class="text-xl">SATS</span></div>
                </div>

                <div class="space-y-3">
                    <div class="swipe-container" id="swipe-container">
                        <div class="swipe-text" id="swipe-text">➔ SWIPE TO PAY NANO</div>
                        <div class="swipe-btn" id="swipe-btn" style="transform: translateX(0px);">
                            <div class="security-ring" id="security-ring"></div>
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-400 text-center font-mono">✦ Powered by Teranode Atomic Mesh Ledger</div>
                </div>
            </div>

            <div class="mt-8 pt-5 border-t border-white/10 text-center">
                <span class="text-[10px] text-slate-500 font-mono uppercase">QLUX GLOBAL APEX ENTERPRISE SYSTEM</span>
            </div>
        </div>
    </main>

    <footer class="mt-14 border-t border-white/10 pt-6 text-center text-slate-500 text-xs font-mono">
        &copy; QLUX GLOBAL ENTERPRISE APEX HUB. ALL RIGHTS RESERVED.
    </footer>
</div>

<script>
// リアルタイム時計とハッシュの更新シミュレーション
setInterval(() => {
    const now = new Date();
    document.getElementById('live-clock').innerText = now.toISOString().slice(11, 19) + " UTC";
    const randomHash = "0x" + Array.from({length: 8}, () => Math.floor(Math.random()*16).toString(16)).join('') + "..." + Array.from({length: 6}, () => Math.floor(Math.random()*16).toString(16)).join('');
    document.getElementById('live-merkle').innerText = randomHash;
}, 1000);

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
    document.getElementById('selected-price').innerHTML = `${price} <span class="text-xl">SATS</span>`;
}

// 超高級スワイプボタンの滑らかなロジック
const container = document.getElementById('swipe-container');
const btn = document.getElementById('swipe-btn');
const text = document.getElementById('swipe-text');
const ring = document.getElementById('security-ring');

let isDragging = false;
let startX = 0;
let currentX = 0;
let maxTranslate = 0;

function updateMaxTranslate() {
    maxTranslate = container.clientWidth - btn.clientWidth - 12;
}
window.addEventListener('resize', updateMaxTranslate);
window.addEventListener('load', updateMaxTranslate);

function handleStart(e) {
    if (btn.classList.contains('processing') || btn.classList.contains('unlocked')) return;
    isDragging = true;
    startX = (e.touches ? e.touches[0].clientX : e.clientX) - currentX;
    btn.classList.add('sliding');
    text.classList.add('hide');
}

function handleMove(e) {
    if (!isDragging) return;
    updateMaxTranslate();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    currentX = clientX - startX;
    if (currentX < 0) currentX = 0;
    if (currentX > maxTranslate) currentX = maxTranslate;
    btn.style.transform = `translateX(${currentX}px)`;
}

function handleEnd() {
    if (!isDragging) return;
    isDragging = false;
    btn.classList.remove('sliding');
    updateMaxTranslate();

    if (currentX >= maxTranslate * 0.85) {
        btn.style.transform = `translateX(${maxTranslate}px)`;
        btn.classList.add('unlocked');
        btn.innerHTML = '✓';
        executeNanoPayment();
    } else {
        currentX = 0;
        btn.style.transform = `translateX(0px)`;
        text.classList.remove('hide');
    }
}

btn.addEventListener('mousedown', handleStart);
window.addEventListener('mousemove', handleMove);
window.addEventListener('mouseup', handleEnd);

btn.addEventListener('touchstart', handleStart);
window.addEventListener('touchmove', handleMove);
window.addEventListener('touchend', handleEnd);

async function executeNanoPayment() {
    const userHandle = document.getElementById('user-handle').value;
    const terminal = document.getElementById('execution-terminal');
    const body = document.getElementById('terminal-body');
    const timestamp = document.getElementById('terminal-timestamp');
    
    terminal.style.display = "block";
    timestamp.innerText = new Date().toISOString();
    body.innerHTML = `<span class='text-cyan-400'>[~] Verified. Broadcasting ${selectedPrice} sats nano-payment to Teranode AI Mesh...</span>`;
    
    btn.classList.remove('unlocked');
    btn.classList.add('processing');

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
            btn.classList.remove('processing');
            btn.innerHTML = '⚡';
            currentX = 0;
            btn.style.transform = `translateX(0px)`;
            text.classList.remove('hide');

            body.innerHTML = `
                <div><span class='text-slate-400'>ACQUIRED ASSET:</span> <strong class='text-white'>${data.asset_name}</strong></div>
                <div><span class='text-slate-400'>AI CONSUMER:</span> <strong class='text-amber-400'>${data.user_handle}</strong></div>
                <div><span class='text-slate-400'>SETTLED AMOUNT:</span> <strong class='text-emerald-400 font-mono'>${data.price_sats} SATS</strong></div>
                <div><span class='text-slate-400'>ATOMIC TXID:</span> <code class='text-cyan-300'>${data.txid_hash}</code></div>
                <div class='mt-2 pt-2 border-t border-white/10 text-emerald-400 font-bold'>[✓] STREAM DECRYPTED & SYNCED WITH AI MESH.</div>
            `;
        }, 500);
    } catch (err) {
        btn.classList.remove('processing');
        btn.innerHTML = '⚡';
        currentX = 0;
        btn.style.transform = `translateX(0px)`;
        text.classList.remove('hide');
        body.innerHTML = "<span class='text-red-400'>[!] Error: Teranode consensus timeout.</span>";
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
            price_sats = data.get("price_sats", 15)
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
            self.send_header("Content-Type", "application/json; charset=u
