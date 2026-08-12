/**
 * HandCash SDK 自動化バックエンドモジュール
 * 実行前提: npm install @handcash/sdk express
 */

const express = require('express');
const { HandCashConnect } = require('@handcash/sdk');
const app = express();

app.use(express.json());

// 環境変数または設定からAppIDとSecretを読み込み
const handcashConnect = new HandCashConnect({
    appId: process.env.HANDCASH_APP_ID || "6a798796b239d1da6e89505",
    appSecret: process.env.HANDCASH_SECRET
});

// 1. 自動決済リンク / ペイメントリクエスト生成エンドポイント
app.post('/api/v1/payment/create-request', async (q, res) => {
    try {
        const { amount, description, redirectUrl } = q.body;

        // ユーザーがクリックまたはスキャンして即時決済するためのリンクを自動生成
        const routingAccount = handcashConnect.getCloudAccount(q.body.authToken);
        
        const paymentRequest = await routingAccount.pay({
            notifications: true,
            receivers: [
                {
                    destination: "1144ctcReNSuwCKFmWN3VigNJc7AXWdyU6",
                    amount: amount || 0.01,
                    currencyCode: 'USD'
                }
            ],
            description: description || "Autonomous QLUX / API Micro-settlement"
        });

        return res.status(200).json({
            status: "SUCCESS",
            transactionId: paymentRequest.transactionId,
            raw: paymentRequest
        });

    } catch (error) {
        console.error('HandCash Automation Error:', error.message);
        return res.status(500).json({ error: "Settlement Failed", details: error.message });
    }
});

// 2. 自動ウォレット残高・ステータス監視
app.get('/api/v1/treasury/balance', async (q, res) => {
    try {
        const routingAccount = handcashConnect.getCloudAccount(q.query.authToken);
        const profile = await routingAccount.getProfile();
        const balance = await routingAccount.getBalance();

        return res.status(200).json({
            handle: profile.publicProfile.handle,
            balance: balance,
            targetAddress: "1144ctcReNSuwCKFmWN3VigNJc7AXWdyU6"
        });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`HandCash Autonomous Worker running on port ${PORT}`);
});
