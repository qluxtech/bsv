import os
import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_CODE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX APEX - Enterprise On-Chain Exchange</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
body { background-color: #000205; color: #ffffff; font-family: sans-serif; }
.card { background: rgba(8, 14, 28, 0.95); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 20px; padding: 24px; }
.swipe-box { position: relative; width: 100%; height: 75px; background: rgba(255,255,255,0.05); border-radius: 18px; border: 1px solid #f59e0b; overflow: hidden; user-select: none; }
.swipe-btn { position: absolute; left: 4px; top: 4px; width: 67px; height: 67px; background: #f59e0b; border-radius: 14px; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold; cursor: pointer; transition: background 0.2s; z-index: 10; }
.swipe-btn.unlocked { background: #10b981; color: #fff; }
.swipe-text { position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; color: #fbbf24; letter-spacing: 0.1em; }
</style>
</head>
<body class="min-h-screen p-4 sm:p-8">

<div class="max-w-4xl mx-auto space-y-6">
    <div class="card text-center">
        <h1 class="text-2xl sm:text-3xl font-black text-amber-400 mb-2">QLUX APEX ON-CHAIN HUB</h1>
        <p class="text-sm text-slate-400">AI & Enterprise High-Value Data & Nano-Payment Gateway</p>
    </div>

    <div class="card space-y-4">
        <h2 class="text-lg font-bold text-amber-400">Teranode AI Telemetry Stream</h2>
        <div class="bg-black/80 border border-cyan-500/30 rounded-xl p-4 font-mono text-xs space-y-2">
            <div class="text-cyan-400 font-bold">[LIVE FEED: ACTIVE]</div>
            <div class="text-slate-300">Active AI Swarm Consumers: <span class="text-amber-400">14,892 Nodes</span></div>
            <div class="text-slate-300">Throughput Velocity: <span class="text-emerald-400">1,420,000 TPS</span></div>
        </div>

        <div>
            <label class="block text-xs font-bold text-amber-400 mb-1">AI Agent Handle ID</label>
            <input type="text" id="user-handle" value="$qlux_ai_agent" class="w-full bg-black border border-white/20 rounded-lg px-3 py-2 text-white font-mono text-sm">
        </div>

        <div id="terminal" class="bg-black border border-cyan-500/50 rounded-xl p-4 font-mono text-xs hidden">
            <div class="text-cyan-400 font-bold mb-1">DATA UNLOCKED SUCCESSFULLY</div>
            <div id="terminal-body" class="text-slate-300 break-all"></div>
        </div>
    </div>

    <div class="card space-y-4">
        <h3 class="text-md font-bold text-white">Swipe Nano-Payment (15 Sats)</h3>
        <div class="swipe-box" id="swipe-container">
            <div class="swipe-text" id="swipe-text">SWIPE RIGHT TO PAY & UNLOCK &rarr;</div>
            <div class="swipe-btn" id="swipe-btn">&rarr;</div>
        </div>
    </div>
</div>

<script>
const container = document.getElementById('swipe-container');
const btn = document.getElementById('swipe-btn');
const text = document.getElementById('swipe-text');

let dragging = false;
let startX = 0;
let currentX = 0;
let maxDist = 0;

function getMax() {
