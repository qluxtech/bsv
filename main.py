import os
import json
import hashlib
import time
import socketserver
from http.server import SimpleHTTPRequestHandler, HTTPServer

# HTMLを外部ファイルとして自動生成することでPythonの構文エラーを100%回避
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX BSV APEX - World's #1 Teranode Data Exchange & Swarm Hub</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        void: '#000205',
        glass: 'rgba(8, 14, 28, 0.95)',
        bsvgold: { 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706' }
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
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center font-black text-black text-2xl shadow-xl shadow-amber-500/40">⚡</div>
            <div>
                <span class="text-2xl font-black tracking-widest bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">QLUX BSV APEX</span>
                <span class="block text-[10px] text-amber-400 tracking-widest font-mono uppercase">Bitcoin SV Teranode Global Data & Nano-Payment Exchange</span>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <button onclick="openModal('upload-modal')" class="px-4 py-2 rounded-full bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20">
                + BSVデータを出品する
            </button>
            <button onclick="openModal('sub-modal')" class="px-4 py-2 rounded-full bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-400 font-bold text-xs uppercase tracking-wider transition-all">
                👑 VIP会員サブスク
            </button>
        </div>
    </header>

    <section class="text-center max-w-4xl mx-auto pt-2 pb-2">
        <h1 class="text-3xl sm:text-5xl font-black tracking-tight mb-4 leading-tight">
            BSV Teranodeが生む無限のスケール、<br><span class="bg-gradient-to-r from-amber-400 via-yellow-200 to-amber-500 bg-clip-text text-transparent">世界中のオンチェーンデータを1スワイプ取引。</span>
        </h1>
        <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            世界中のベンダーがBSVチェーン上にアップロードした超高精度データを一元化。サトシ単位のナノペイメントとサブスクで完全にエコシステム化。
        </p>
    </section>

    <section class="max-w-5xl mx-auto">
        <div class="matrix-screen matrix-grid p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4 border-b border-emerald-500/20 pb-4">
                <div class="flex items-center space-x-3">
                    <div class="pulse-dot"></div>
                    <div>
                        <h3 class="text-sm sm:text-base font-bold text-emerald-400 font-mono tracking-wider">BSV TERANODE ATOMIC MESH MONITOR</h3>
                        <p class="text-[11px] text-slate-400 font-mono">Global Sharding & Zero-Fee Micro-Tx Stream</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3 font-mono text-xs">
                    <span class="px-3 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">BSV BLOCK: #842,915</span>
                    <span class="px-3 py-1 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" id="matrix-timer">00:00:00 UTC</span>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div class="bg-black/60 border border-emerald-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>TERANODE TPS</span>
                        <span class="text-emerald-400 font-bold">UNLIMITED</span>
                    </div>
                    <div class="text-2xl font-black text-white">1,420,310 <span class="text-xs text-emerald-400">TPS</span></div>
                    <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-emerald-500 to-cyan-400 h-full w-[88%] animate-pulse"></div>
                    </div>
                </div>
                <div class="bg-black/60 border border-amber-500/30 rounded-2xl p-5 space-y-3 font-mono">
                    <div class="text-xs text-slate-400 flex justify-between">
                        <span>GLOBAL VENDORS</span>
                        <span class="text-amber-400 font-bold">ACTIVE</span>
                    </div>
                    <div class="text-2xl font-black text-white">5,120 <
