import requests
import json
import time

# あなたのRender上で稼働しているURL（例）
TARGET_URL = "https://bsv-xxxx.onrender.com/api/v1/omni/execute"
# または、ローカルテスト用
# TARGET_URL = "http://localhost:10000/api/v1/omni/execute"

SERVICES = ["data_query", "ai_prompt", "storage_write", "auction_settle"]
TOKENS = ["ai_agent_alpha_premium", "ai_agent_beta_standard"]

def run_external_agent_simulation():
    print("=== External AI Agent Mesh Client Started ===")
    
    while True:
        service = SERVICES[int(time.time()) % len(SERVICES)]
        token = TOKENS[int(time.time()) % len(TOKENS)]
        
        headers = {
            "Content-Type": "application/json",
            "X-Payment-Token": token
        }
        
        payload = {
            "service_type": service,
            "payload": {
                "query": "global_liquidity_index",
                "prompt": "Analyze autonomous cross-border payment efficiency",
                "key": f"ext_record_{int(time.time())}",
                "value": {"status": "verified_external", "timestamp": time.time()}
            }
        }
        
        try:
            print(f"-> Sending Request: Service [{service}] with Token [{token}]...")
            res = requests.post(TARGET_URL, headers=headers, json=payload, timeout=5)
            print(f"<- Response Status: {res.status_code}")
            print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Connection/Network Error: {e}")
            
        print("-" * 50)
        time.sleep(3)

if __name__ == "__main__":
    run_external_agent_simulation()

