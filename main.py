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
<title>QLUX APEX - Global On-Chain Data Exchange & Subscription Hub</title>
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
.gold-glow { box-shadow: 0 0 100px rgba(245, 158, 11, 0.25); }
.gold-border { border-color: rgba(245, 158, 11, 0.6); }

.matrix-screen {
  background: radial-gradient(circle at center, rgba(16, 185, 129, 0.1) 0%, rgba(0, 2, 5, 0.95) 80%);
  border: 1px solid rgba(52, 211, 153, 0.4);
  box-shadow: inset 0 0 30px rgba(52, 211, 153, 0.15), 0 0 40px rgba(52, 211, 153, 0.1);
  border-radius: 24px;
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
  position: relative; width: 100%; height: 75px; background: rgba(0, 0, 0, 0.7);
  border-radius: 20px; padding: 6px; overflow: hidden; user-select: none;
  border: 1px solid rgba(245, 158, 11, 0.4); box-shadow: inset 0 4px 20px rgba(0,0,0,0.8), 0 0 30px rgba(245,158,11,0.15);
}
.swipe-btn {
  position: absolute; left: 6px; top: 6px; width: 63px; height: 63px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
  border-radius: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center;
  color: #000205; font-size: 22px; font-weight: bold; box-shadow: 0 6px 25px rgba(245, 158, 11, 0.5);
  transition: background 0.2s ease; z-index: 10;
}
.swipe-btn.unlocked { background: linear-gradient(135deg, #34d399 0%, #059669 100%); color: #ffffff; }
.swipe-text {
  position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em;
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
                <span class="block text-[10px] text-amber-400 tracking-widest font-mono uppercase">Global On-Chain Data Exchange & Subscription Hub</span>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <button onclick="openModal('upload-modal')" class="px-4 py-2 rounded-full bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20">
                + データを出品する
            </button>
            <button onclick="openModal('sub-modal')" class="px-4 py-2 rounded-full bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-400 font-bold text-xs uppercase tracking-wider transition-all">
                👑 VIP会員・サブスク
            </button>
        </div>
    </header>

    <section class="text-center max-w-4xl mx-auto pt-2 pb-2">
        <h1 class="text-3xl sm:text-5xl font-black tracking-tight mb-4 leading-tight">
            世界中からオンチェーンデータを集結、<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">1スワイプで即座に取引。</span>
        </h1>
        <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            世界中のベンダーが出品した超高精度データをその場で閲覧・購入。会員はサブスクリプションで全データが使い放題に。
        </p>
    </section>

    <section class="max-w-5xl mx-auto">
        <div class="matrix-screen matrix-grid p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4 border-b border-emerald-500/20 pb-4">
                <div class="flex items-center space-x-3">
                    <div class="pulse-dot"></div>
                    <div>
                        <h3 class="text-sm sm:text-base font-bold text-emerald-400 font-mono tracking-wider">GLOBAL ON-CHAIN DATA STREAM MONITOR</h3>
                        <p class="text-[11px] text-slate-400 font-mono">Teranode Atomic Mesh & Global Vendor Sync</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3 font-mono text-xs">
                    <span class="px-3 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">ACTIVE ASSETS: 1,248</span>
                    <span class="px-3 py-1 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" id="matrix-timer">00:00:00 UTC</span>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div class="bg-black/60 border border-emerald-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>GLOBAL TPS VELOCITY</span>
                        <span class="text-emerald-400 font-bold">LIVE</span>
                    </div>
                    <div class="text-2xl font-black text-white" id="stat-tps">1,420,310 <span class="text-xs text-emerald-400">TPS</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-emerald-500 to-cyan-400 h-full w-[85%] animate-pulse"></div>
                    </div>
                </div>

                <div class="bg-black/60 border border-amber-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>REGISTERED VENDORS</span>
                        <span class="text-amber-400 font-bold">GLOBAL</span>
                    </div>
                    <div class="text-2xl font-black text-white">4,892 <span class="text-xs text-amber-400">PEERS</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-amber-500 to-yellow-300 h-full w-[92%] animate-pulse"></div>
                    </div>
                </div>

                <div class="bg-black/60 border border-cyan-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>SUB-SCRIBERS</span>
                        <span class="text-cyan-400 font-bold">VIP UNLOCKED</span>
                    </div>
                    <div class="text-2xl font-black text-white">12,400+ <span class="text-xs text-cyan-400">USERS</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-cyan-500 to-blue-500 h-full w-[98%] animate-pulse"></div>
                    </div>
                </div>
            </div>

            <div class="bg-black/80 rounded-xl p-4 border border-emerald-500/20 font-mono text-xs text-emerald-300/90 h-20 overflow-y-auto space-y-1" id="packet-log">
                <div>[08:35:01] NEW VENDOR UPLOADED: TOKYO_AI_TELEMETRY_v4.dat</div>
                <div>[08:35:02] SUBSCRIPTION RENEWED FOR MEMBER #9921 ($QLUX_VIP)</div>
                <div>[08:35:04] NANO-PAYMENT 15 SATS SETTLED VIA 1-SWIPE BAR</div>
            </div>
        </div>
    </section>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-3xl p-6 sm:p-8 gold-border space-y-6">
            <h2 class="text-lg font-bold flex items-center text-amber-400">Featured On-Chain Market Assets</h2>
            
            <div class="space-y-3">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80">Select Data Asset for 1-Swipe Purchase</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3" id="asset-list">
                    <div onclick="selectAsset(this, 'Tokyo AI Neural Telemetry Stream', 15, 'Vendor: $tokyo_node')" class="asset-card cursor-pointer border border-amber-500 bg-amber-500/10 rounded-2xl p-4 transition-all">
                        <div class="text-sm font-bold text-white mb-1">Tokyo AI Neural Telemetry</div>
                        <div class="text-xs text-slate-400 mb-2">Vendor: $tokyo_node</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">15 Sats</div>
                    </div>
                    <div onclick="selectAsset(this, 'Silicon Valley Atomic Ledger Feed', 30, 'Vendor: $sv_metrics')" class="asset-card cursor-pointer border border-white/10 bg-black/40 rounded-2xl p-4 transition-all">
                        <div class="text-sm font-bold text-white mb-1">Silicon Valley Atomic Ledger</div>
                        <div class="text-xs text-slate-400 mb-2">Vendor: $sv_metrics</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">30 Sats</div>
                    </div>
                </div>
            </div>

            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-2">Your Handle ID / Member ID</label>
                <input type="text" id="user-handle" value="$qlux_member" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-amber-500">
            </div>

            <div id="execution-terminal" class="bg-black/95 border border-cyan-500/40 rounded-2xl p-5 font-mono text-xs hidden space-y-2">
                <div class="text-cyan-400 font-bold">DATA UNLOCKED SUCCESSFULLY</div>
                <div id="terminal-body" class="text-slate-300 break-all space-y-1"></div>
            </div>
        </div>

        <div class="glass-card rounded-3xl p-6 sm:p-8 flex flex-col justify-between gold-glow gold-border space-y-6">
            <div class="space-y-6">
                <div>
                    <h3 class="text-lg font-bold mb-2 text-white">1-Swipe Instant Payment</h3>
                    <p class="text-xs text-slate-400">バーを右端までスワイプして、ナノペイメントで即座にデータ購入・閲覧権を獲得します。</p>
                </div>

                <div class="bg-white/5 rounded-2xl p-5 border border-white/5 text-center">
                    <div class="text-slate-400 text-xs uppercase tracking-wider mb-1">Price</div>
                    <div id="selected-price" class="text-4xl font-black text-amber-400 font-mono">15 <span class="text-xl">SATS</span></div>
                </div>

                <div class="space-y-3">
                    <div class="swipe-container" id="swipe-container">
                        <div class="swipe-text" id="swipe-text">SWIPE TO BUY &rarr;</div>
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

<div id="upload-modal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4 z-50">
    <div class="glass-card rounded-3xl p-6 sm:p-8 max-w-lg w-full gold-border space-y-5">
        <div class="flex justify-between items-center border-b border-white/10 pb-4">
            <h3 class="text-lg font-bold text-amber-400">世界中からオンチェーンデータを出品</h3>
            <button onclick="closeModal('upload-modal')" class="text-slate-400 hover:text-white font-bold">✕</button>
        </div>
        <div class="space-y-4 text-xs">
            <div>
                <label class="block text-slate-300 font-bold mb-1">データ名称 (Asset Title)</label>
                <input type="text" id="up-title" placeholder="例: London AI Swarm Telemetry" class="w-full bg-black/80 border border-white/20 rounded-xl px-3 py-2 text-white font-mono">
            </div>
            <div>
                <label class="block text-slate-300 font-bold mb-1">出品者ハンドル (Vendor Handle)</label>
                <input type="text" id="up-vendor" value="$my_vendor" class="w-full bg-black/80 border border-white/20 rounded-xl px-3 py-2 text-white font-mono">
            </div>
            <div>
                <label class="block text-slate-300 font-bold mb-1">希望価格 (Sats)</label>
                <input type="number" id="up-price" value="20" class="w-full bg-black/80 border border-white/20 rounded-xl px-3 py-2 text-white font-mono">
            </div>
            <button onclick="submitAsset()" class="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-black text-sm uppercase transition-all shadow-lg">
                マーケットに出品する
            </button>
        </div>
    </div>
</div>

<div id="sub-modal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden items-center justify-center p-4 z-50">
    <div class="glass-card rounded-3xl p-6 sm:p-8 max-w-lg w-full gold-border space-y-5">
        <div class="flex justify-between items-center border-b border-white/10 pb-4">
            <h3 class="text-lg font-bold text-emerald-400">VIP会員 サブスクリプションプラン</h3>
            <button onclick="closeModal('sub-modal')" class="text-slate-400 hover:text-white font-bold">✕</button>
        </div>
        <div class="space-y-4 text-xs">
            <div class="bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-4 space-y-2">
                <div class="text-emerald-400 font-bold text-sm">👑 VIP UNLIMITED PASS</div>
                <div class="text-slate-300">月額 1,000 Satsで、世界中のすべてのオンチェーンデータがスワイプ不要でダウンロード・閲覧し放題になります。</div>
            </div>
            <button onclick="alert('VIPサブスクが有効化されました！全データにアクセス可能です。'); closeModal('sub-modal');" class="w-full py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-black text-sm uppercase transition-all shadow-lg">
                VIPサブスクに加入する
            </button>
        </div>
    </div>
</div>

<script>
function openModal(id) { document.getElementById(id).classList.remove('hidden'); document.getElementById(id).classList.add('flex'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); document.getElementById(id).classList.remove('flex'); }

let selectedPrice = 15;
let selectedAssetName = "Tokyo AI Neural Telemetry Stream";

function selectAsset(element, assetName, price, vendor) {
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

function submitAsset() {
    const title = document.getElementById('up-title').value || 'Custom On-Chain Data';
    const vendor = document.getElementById('up-vendor').value || '$vendor';
    const price = parseInt(document.getElementById('up-price').value) || 20;

    const list = document.getElementById('asset-list');
    const div = document.createElement('div');
    div.className = 'asset-card cursor-pointer border border-white/10 bg-black/40 rounded-2xl p-4 transition-all';
    div.setAttribute('onclick', "selectAsset(this, '" + title + "', " + price + ", 'Vendor: " + vendor + "')");
    div.innerHTML = '<div class="text-sm font-bold text-white mb-1">' + title + '</div><div class="text-xs text-slate-400 mb-2">Vendor: ' + vendor + '</div><div class="text-amber-400 font-mono font-bold text-sm">' + price + ' Sats</div>';
    list.appendChild(div);

    closeModal('upload-modal');
    alert('データが正常に出品されました！マーケットに追加されました。');
}

// ライブ時計とログ
setInterval(() => {
    const now = new Date();
    document.getElementById('matrix-timer').innerText = now.toISOString().slice(11, 19) + " UTC";
}, 1000);

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
            headers: { 'Content-Type':
