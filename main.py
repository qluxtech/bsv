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
<title>QLUX APEX — Ultimate On-Chain Data Exchange & Swipe Nano-Payments</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        void: '#000205',
        glass: 'rgba(8, 14, 28, 0.92)',
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
.glass-card { background: rgba(8, 14, 28, 0.92); backdrop-filter: blur(30px); border: 1px solid rgba(255, 255, 255, 0.08); }
.gold-glow { box-shadow: 0 0 80px rgba(245, 158, 11, 0.25); }
.gold-border { border-color: rgba(245, 158, 11, 0.6); }

/* 超進化スワイプボタンのスタイル */
.swipe-container {
  position: relative; width: 100%; height: 80px; background: rgba(255, 255, 255, 0.05);
  border-radius: 20px; padding: 5px; overflow: hidden; user-select: none;
  border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
}
.swipe-btn {
  position: absolute; left: 5px; top: 5px; width: 70px; height: 70px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 16px; cursor: grab; display: flex; align-items: center; justify-content: center;
  color: #000205; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
  transition: transform 0.1s ease, background 0.3s ease, box-shadow 0.3s ease;
  z-index: 10;
}
.swipe-btn:active { cursor: grabbing; }
.swipe-btn.unlocked { background: #10b981; color: #ffffff; transform: scale(1.02); }
.swipe-btn.processing { background: #06b6d4; color: #ffffff; animation: pulse 1.5s infinite; cursor: wait;}
.swipe-text {
  position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em;
  background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
  background-size: 200% auto; color: transparent; -webkit-background-clip: text;
  background-clip: text; animation: shine 3s linear infinite; opacity: 1; transition: opacity 0.3s;
}
.swipe-text.hide { opacity: 0; }

/* セキュリティ・リングアニメーション */
.security-ring {
  position: absolute; top: -5px; left: -5px; width: 80px; height: 80px;
  border: 3px solid transparent; border-top-color: #f59e0b; border-radius: 20px;
  opacity: 0; transition: opacity 0.3s;
}
.swipe-btn.sliding .security-ring { opacity: 1; animation: spin 1s linear infinite; }

@keyframes shine { to { background-position: 200% center; } }
@keyframes spin { 100% { transform: rotate(360deg); } }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 15px #06b6d4; } 50% { box-shadow: 0 0 30px #06b6d4; } }
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
            <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center font-black text-black text-xl shadow-lg shadow-amber-500/30">Q</div>
            <div>
                <span class="text-2xl font-black tracking-widest bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">QLUX APEX</span>
                <span class="block text-[10px] text-amber-400 tracking-widest font-mono uppercase">On-Chain Data Exchange & Teranode Nano-Payment Hub</span>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <div class="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[11px] font-bold">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>TERANODE POWERED</span>
            </div>
            <div class="px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[11px] font-bold uppercase tracking-wider">
                GLOBAL APEX
            </div>
        </div>
    </header>

    <section class="text-center max-w-3xl mx-auto mb-10">
        <div class="inline-block px-4 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[10px] font-extrabold tracking-widest uppercase mb-3">
            Next-Gen On-Chain Data Monetization
        </div>
        <h1 class="text-3xl sm:text-4xl font-black tracking-tight mb-3 leading-tight">
            秒速ナノペイメントで開く、<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">高価値エンタープライズ・データへのゲートウェイ。</span>
        </h1>
        <p class="text-slate-400 text-sm font-normal max-w-xl mx-auto leading-relaxed">
            ワン・スワイプの超少額決済（ナノペイメント）で、世界中のオンチェーン・データ資産をミリ秒単位で即座に購入・購読・収益化。
        </p>
    </section>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-3xl p-7 gold-border">
            <h2 class="text-lg font-bold mb-5 flex items-center text-amber-400">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                Data Exchange Marketplace
            </h2>

            <div class="space-y-3 mb-5">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80">Select Monetized Data Asset</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div onclick="selectAsset(this, 'Teranode Global Hash Telemetry', 10)" class="asset-card cursor-pointer border border-amber-500/50 bg-amber-500/10 rounded-2xl p-3 transition-all hover:border-amber-400">
                        <div class="text-sm font-bold text-white mb-0.5">Teranode Hash Telemetry</div>
                        <div class="text-xs text-slate-400 mb-2">リアルタイム・ノードパフォーマンスデータ</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">⚡ 10 Sats / Query</div>
                    </div>
                    <div onclick="selectAsset(this, 'BSV Atomic Smart Contract Feed', 25)" class="asset-card cursor-pointer border border-white/10 bg-black/40 rounded-2xl p-3 transition-all hover:border-amber-400">
                        <div class="text-sm font-bold text-white mb-0.5">Atomic State Feed</div>
                        <div class="text-xs text-slate-400 mb-2">クロスチェーン・アトミック状態証明</div>
                        <div class="text-amber-400 font-mono font-bold text-sm">⚡ 25 Sats / Query</div>
                    </div>
                </div>
            </div>

            <div class="mb-5">
                <label class="block text-xs font-bold uppercase tracking-wider text-amber-400/80 mb-1.5">Buyer / Node Handle ID</label>
                <input type="text" id="user-handle" value="$qlux_global_apex_trader" class="w-full bg-black/80 border border-white/20 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-amber-500 transition-colors">
            </div>

            <div id="execution-terminal" class="mt-5 bg-black/95 border border-cyan-500/40 rounded-2xl p-5 font-mono text-xs hidden">
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

        <div class="glass-card rounded-3xl p-7 flex flex-col justify-between gold-glow gold-border">
            <div>
                <h3 class="text-lg font-bold mb-5 text-white flex items-center">
                    <svg class="w-5 h-5 mr-2 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    Swipe to Pay & Unlock Data
                </h3>
                <div class="bg-white/5 rounded-2xl p-4 border border-white/5 mb-5 text-center">
                    <div class="text-slate-400 text-[11px] uppercase tracking-wider mb-0.5">Selected Asset Price</div>
                    <div id="selected-price" class="text-4xl font-black text-amber-400 font-mono">10 <span class="text-2xl">SATS</span></div>
                </div>

                <div class="swipe-container" id="swipe-container">
                    <div class="swipe-text" id="swipe-text">⚡ SWIPE TO PAY NANO</div>
                    <div class="swipe-btn
