const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const QLUX_CONFIG = {
    appId: process.env.APP_ID,
    authToken: process.env.AUTH_TOKEN,
    legacyAddress: process.env.VAULT_ADDRESS,
    apiBaseUrl: 'https://cloud.handcash.io/v2'
};

// フロントエンド画面の配信（余計なバックエンドコードは一切含めない綺麗なHTML）
app.get('/', (req, res) => {
    res.send(`<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QLUX — SANCTUARY [ONCHAIN FORTRESS]</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body { background-color: #050a0f; color: #c0d5e0; font-family: 'Courier New', Courier, monospace; padding: 15px; display: flex; flex-direction: column; align-items: center; }
        .outer-frame { width: 100%; max-width: 620px; border: 1px solid rgba(0, 229, 255, 0.4); border-radius: 12px; padding: 24px 18px; background: #050a0f; box-shadow: 0 0 25px rgba(0, 229, 255, 0.15); display: flex; flex-direction: column; gap: 25px; text-align: center; }
        .brand-title { font-size: 26px; color: #00e5ff; font-weight: bold; letter-spacing: 3px; margin-bottom: 6px; text-shadow: 0 0 12px rgba(0, 229, 255, 0.4); }
        .main-banner { background: linear-gradient(135deg, #00e5ff, #00bcd4); color: #03080d; padding: 18px 12px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .terminal-logs { font-size: 10px; color: #00e5ff; background: #010305; padding: 10px; border-radius: 5px; height: 130px; overflow-y: hidden; text-align: left; line-height: 1.6; }
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(3, 8, 13, 0.85); display: none; justify-content: center; align-items: center; z-index: 999; padding: 20px; }
        .modal-content { background: #071018; border: 1px solid #00e5ff; border-radius: 12px; padding: 24px; width: 100%; max-width: 500px; text-align: left; }
        .modal-input { width: 100%; background: #030609; border: 1px solid #1e3a4c; color: #e0f7fa; padding: 10px; border-radius: 6px; font-family: inherit; font-size: 12px; margin-bottom: 16px; height: 80px; }
        .btn { background: #071018; border: 1px solid #00e5ff; color: #00e5ff; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn-primary { background: #00e5ff; color: #03080d; }
    </style>
</head>
<body>
    <div class="outer-frame">
        <div class="brand-header">
            <div style="font-size: 10.5px; color: #00bcd4; letter-spacing: 2px;">ABSOLUTE SOVEREIGNTY // WEBSERVICE</div>
            <div class="brand-title">QLUX</div>
            <div style="font-size: 12px; color: #90a4ae;">BSVブロックチェーン要塞 & マイクロペイメントエンジン</div>
        </div>
        <div class="main-banner" id="onchainBtn">
            <div style="font-size: 18px; margin-bottom: 6px;">QLUX ⚡ ONCHAIN</div>
            <div style="font-size: 11.5px; opacity: 0.85;">// クリックしてBSVブロックチェーンへ永久凍結・決済実行</div>
        </div>
        <div style="background: #030609; border: 1px solid #1e3a4c; border-radius: 8px; padding: 14px; text-align: left;">
            <div class="terminal-logs" id="terminalLogs">
                [SYSTEM] Web Service Online & Direct REST Gateway Active.<br>
                [READY] Waiting for payload dispatch...
            </div>
        </div>
    </div>
    <div class="modal-overlay" id="modalOverlay">
        <div class="modal-content">
            <div style="font-size: 16px; color: #00e5ff; margin-bottom: 12px; font-weight: bold;">BSV ONCHAIN DISPATCH</div>
            <textarea class="modal-input" id="payloadInput" placeholder="ブロックチェーンに書き込むデータを入力..."></textarea>
            <div id="statusMsg" style="font-size: 11px; color: #546e7a; margin-bottom: 12px;">Ready to broadcast.</div>
            <div style="display: flex; gap: 10px; justify-content: flex-end;">
                <button class="btn" id="closeModal">キャンセル</button>
                <button class="btn btn-primary" id="executeOnchain">ブロックチェーンへ書込</button>
            </div>
        </div>
    </div>
    <script>
        const btn = document.getElementById('onchainBtn');
        const modal = document.getElementById('modalOverlay');
        const closeBtn = document.getElementById('closeModal');
        const execBtn = document.getElementById('executeOnchain');
        const statusMsg = document.getElementById('statusMsg');
        const payloadInput = document.getElementById('payloadInput');
        const logsContainer = document.getElementById('terminalLogs');

        btn.addEventListener('click', () => modal.style.display = 'flex');
        closeBtn.addEventListener('click', () => modal.style.display = 'none');

        execBtn.addEventListener('click', async () => {
            const data = payloadInput.value.trim();
            if(!data) { alert('データを入力してください'); return; }
            statusMsg.style.color = '#00e5ff';
            statusMsg.innerText = 'HandCash API マイクロペイメント処理中...';

            try {
                const res = await fetch('/api/dispatch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data })
                });
                const result = await res.json();
                if(result.success) {
                    statusMsg.innerText = '永久凍結成功！';
                    logsContainer.innerHTML += '<br>[SUCCESS] TX: ' + result.txId;
                    setTimeout(() => { modal.style.display = 'none'; payloadInput.value = ''; }, 1500);
                } else {
                    statusMsg.style.color = '#ff5252';
                    statusMsg.innerText = 'エラー: ' + result.error;
                }
            } catch(e) {
                statusMsg.style.color = '#ff5252';
                statusMsg.innerText = '通信エラーが発生しました';
            }
        });
    </script>
</body>
</html>`);
});

// バックエンドAPIエンドポイント
app.post('/api/dispatch', async (req, res) => {
    try {
        const { data } = req.body;
        
        const response = await axios.post(
            `${QLUX_CONFIG.apiBaseUrl}/wallet/payments`,
            {
                destination: QLUX_CONFIG.legacyAddress,
                currencyCode: 'BSV',
                amount: 0.00001,
                data: Buffer.from(data).toString('hex')
            },
            {
                headers: {
                    'oauth-token': QLUX_CONFIG.authToken,
                    'client-app-id': QLUX_CONFIG.appId,
                    'Content-Type': 'application/json'
                }
            }
        );

        res.json({ success: true, txId: response.data.transactionId || response.data.txId });
    } catch (error) {
        res.json({ 
            success: false, 
            error: error.response?.data?.message || error.message 
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`QLUX⚡️ONCHAIN Web Service running on port ${PORT}`);
});
