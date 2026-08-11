import urllib.request
import json

def trigger_full_pipeline_test():
    url = "https://qlux-prime.onrender.com/api/v1/pipeline"  # またはローカル環境のURL
    payload = {
        "tier": "professional",
        "intent": "Full_Autonomous_Launch_2026"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    print("⚡ 全モジュール・完全自動パイプラインの起動リクエストを送信中...")
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers, 
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n✅ パイプライン実行成功・全モジュール正常稼働:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n❌ 実行エラー（URLを確認してください）: {e}")

if __name__ == "__main__":
    trigger_full_pipeline_test()
