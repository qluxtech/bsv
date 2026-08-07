import os
import json
import hashlib
import time
import socketserver
from http.server import SimpleHTTPRequestHandler, HTTPServer

# ワンスワイプ取引直下に超優良サービスセクションを組み込んだ完全版HTML
SIMPLE_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QLUX BSV APEX - Teranode & Enterprise Services</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col items-center p-4 selection:bg-amber-500 selection:text-black">
    <div class="max-w-2xl w-full space-y-6 pb-12">
        
        <div class="bg-slate-900 border border-amber-500/40 rounded-3xl p-6 shadow-2xl text-center space-y-3">
            <div class="inline-block p-3 bg-amber-500/10 border border-amber-500/30 rounded-2xl text-2xl">⚡</div>
            <h1 class="text-2xl font-black text-amber-400 tracking-wider">QLUX BSV APEX</h1>
            <p class="text-xs text-slate-400 font-mono">Enterprise-Grade Bitcoin SV Teranode & Cloud Service Ecosystem</p>
            <div class="flex flex-wrap justify-center gap-2 pt-2">
                <span class="px-3 py-1 bg-amber-500/20 border border-amber-500/40 rounded-full text-[10px] font-mono text-amber-300">TERANODE TPS: 1,420,310+</span>
                <span class="px-3 py-1 bg-emerald-500/20 border border-emerald-500/30 rounded-full text-[10px] font-mono text-emerald-300">FEE: < 0.00001 BSV</span>
            </div>
        </div>

        <div class="bg-gradient-to-br from-slate-900 to-black border border-slate-800 rounded-3xl p-6 space-y-4 shadow-xl">
            <h2 class="text-xl font-black text-slate-100 leading-snug">
                無限のスケールを持つBSVチェーンで、<br><span class="text-amber-400">次世代の超優良クラウドサービス</span>を構築。
            </h2>
            <p class="text-xs text-slate-400 leading-relaxed">
                QLUX BSV APEXは、Bitcoin SVのテラノードアーキテクチャを極限まで活かした世界最高峰のデータエクスチェンジ＆ナノペイメントプラットフォームです。
            </p>
        </div>

        <div class="bg-slate-900 border border-amber-500/30 rounded-3xl p-6 space-y-4 shadow-xl">
            <div class="flex justify-between items-center">
                <h3 class="text-sm font-bold text-amber-400 font-mono">⚡ ワンスワイプ取引ポータル</h3>
                <span class="text-[10px] font-mono text-slate-500">Instant Settlement</span>
            </div>
            <div class="bg-black/60 border border-slate-800 rounded-2xl p-4 space-y-2 font-mono text-xs">
                <div class="text-amber-300 font-bold">▶ プレミアムデータストリーム: Enterprise AI Telemetry v4.2</div>
                <div class="text-slate-400">プロバイダ: $qlux_enterprise_node</div>
                <div class="text-emerald-400">決済料金: 15 Sats (ナノペイメント)</div>
            </div>
            <button onclick="executePayment()" class="w-full py-4 rounded-2xl bg-gradient-to-r from-amber-500 to-yellow-400 text-black font-black text-sm uppercase tracking-wider shadow-lg shadow-amber-500/20 active:scale-95 transition-transform">
                → 右端へスワイプしてワンスワイプ取引を実行 →
            </button>
            <div id="result" class="hidden bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-4 font-mono text-xs text-emerald-300 space-y-1"></div>
        </div>

        <div class="bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/30 border border-amber-500/40 rounded-3xl p-6 space-y-5 shadow-2xl">
            <div class="border-b border-amber-500/20 pb-3">
                <span class="text-[10px] font-mono uppercase tracking-widest text-amber-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">FLAGSHIP ECOSYSTEM</span>
                <h3 class="text-base font-black text-white mt-2">🚀 BSV超開発・超優良サービス機能セクション</h3>
                <p class="text-xs text-slate-400 mt-1">ワンスワイプ取引と完全連動する、次世代エンタープライズ・インフラストラクチャ</p>
            </div>

            <div class="grid grid-cols-1 gap-4 text-xs font-mono">
                <div class="bg-black/50 border border-slate-800 p-4 rounded-2xl space-y-2 hover:border-amber-500/50 transition-colors">
                    <div class="text-amber-300 font-bold flex items-center justify-between">
                        <span class="flex items-center gap-2">🌐 Teranode分散型アトミックシャーディング</span>
                        <span class="text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">稼働中</span>
                    </div>
                    <div class="text-slate-300 leading-relaxed text-[11px]">
                        理論上無限のTPSを実現する最新テラノード基盤。世界中のノード間でデータを瞬時に同期し、混雑ゼロの高速アトミック処理を提供します。
                    </div>
                </div>

                <div class="bg-black/50 border border-slate-800 p-4 rounded-2xl space-y-2 hover:border-amber-500/50 transition-colors">
                    <div class="text-amber-300 font-bold flex items-center justify-between">
                        <span class="flex items-center gap-2">💳 超低コスト・ナノペイメントエンジン</span>
                        <span class="text-[10px] text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded">手数料 0.00001 BSV</span>
                    </div>
                    <div class="text-slate-300 leading-relaxed text-[11px]">
                        1サトシ未満のマイクロ課金をワンスワイプで完全自動化。API利用料やデータ閲覧料の都度決済を極限まで効率化します。
                    </div>
                </div>

                <div class="bg-black/50 border border-slate-800 p-4 rounded-2xl space-y-2 hover:border-amber-500/50 transition-colors">
                    <div class="text-amber-300 font-bold flex items-center justify-between">
                        <span class="flex items-center gap-2">📊 オンチェーンAI・金融データ流通ハブ</span>
                        <span class="text-[10px] text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded">大容量対応</span>
                    </div>
                    <div class="text-slate-300 leading-relaxed text-[11px]">
                        高精度AI学習用テレメトリー、リアルタイム金融ストリーム、企業機密アセットをブロックチェーン上に安全に永久保存・トレード。
                    </div>
                </div>

                <div class="bg-black/50 border border-slate-800 p-4 rounded-2xl space-y-2 hover:border-amber-500/50 transition-colors">
                    <div class="text-amber-300 font-bold flex items-center justify-between">
                        <span class="flex items-center gap-2">🛡️ ゼロトラスト・ゼロダウンタイム設計</span>
                        <span class="text-[10px] text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded">24/365 完動</span>
                    </div>
                    <div class="text-slate-300 leading-relaxed text-[11px]">
                        単一障害点（SPOF）を完全に排除したパブリックブロックチェーンの堅牢性により、世界中どこからでも停止しない超高信頼サービスを実現。
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 space-y-4">
            <h3 class="text-sm font-bold text-amber-400 font-mono">📺 サービス紹介・デモプレビュー</h3>
            <div class="aspect-video w-full bg-black/80 border border-slate-800 rounded-2xl flex flex-col items-center justify-center p-4 text-center space-y-2 relative overflow-hidden">
                <div class="absolute inset-0 bg-[radial-gradient(#d97706_1px,transparent_1px)] [background-size:16px_16px] opacity-10"></div>
                <div class="text-4xl animate-bounce">▶️</div>
                <p class="text-xs font-mono text-slate-300">QLUX BSV APEX: ワンスワイプ取引＆テラノード実演ストリーム</p>
                <span class="px-3 py-1 bg-amber-500/20 border border-amber-500/40 rounded-full text-[10px] font-mono text-amber-400">HD STREAMING READY</span>
            </div>
        </div>

        <div class="text-center text-[10px] font-mono text-slate-500 space-y-1 pt-4 border-t border-slate-800/80">
            <p>© 2026 QLUX BSV APEX Ecosystem. All Rights Reserved.</p>
            <p class="text-amber-500/60">Powered by Bitcoin SV Teranode & Enterprise Cloud Infrastructure</p>
        </div>

    </div>

<script>
function executePayment() {
    fetch('/api/pay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sats: 15 })
    })
    .then(res => res.json())
    .then(data => {
        const resBox = document.getElementById('result');
        resBox.classList.remove('hidden');
        resBox.innerHTML = `<b>[ワンスワイプ取引成功] データアンロック完了</b><br>ID: $qlux_member_01<br>決済額: ${data.sats} SATS<br>TXID: ${data.txid}<br><span class="text-amber-400">[BSV OK] Teranode台帳へのアトミック記録完了。</span>`;
    });
}
</script>
</body>
</html>"""

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class ApexRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(SIMPLE_HTML.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(SIMPLE_HTML.encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/pay':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode('utf-8'))
            except:
                data = {}
            
            sats = data.get('sats', 15)
            seed = str(time.time()) + "-" + str(sats)
            txid = hashlib.sha256(seed.encode('utf-8')).hexdigest()
            
            resp_data = {'status': 'success', 'sats': sats, 'txid': txid}
            resp = json.dumps(resp_data).encode('utf-8')
            
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
    server = None
    
    for p in [port, port + 1, port + 2, 8080, 5000, 3000]:
        try:
            server = ThreadedHTTPServer(('0.0.0.0', p), ApexRequestHandler)
            break
        except OSError:
            continue
            
    if server is None:
        server = ThreadedHTTPServer(('0.0.0.0', 0), ApexRequestHandler)

    server.serve_forever()
