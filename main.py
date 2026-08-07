from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

app = FastAPI(title="QLUX APEX All-On-Chain Teranode & Exchange")

class PaymentRequest(BaseModel):
    sats: int = 5000
    fiat: str = "50 USD"

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        if os.path.exists("index.html"):
            with open("index.html", "r", encoding="utf-8") as f:
                return f.read()
        return "<h1>index.html not found in working directory.</h1>"
    except Exception as e:
        return f"<h1>Server Error: {str(e)}</h1>"

@app.post("/api/pay")
def process_payment(req: PaymentRequest):
    try:
        return {
            "status": "success",
            "sats": req.sats,
            "fiat": req.fiat,
            "txid": "0x49f8c41e9b21a820c78e21950e2621ad79f8b41"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
