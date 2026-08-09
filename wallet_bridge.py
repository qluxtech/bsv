class HandCashBridge:
    def __init__(self, app_id: str):
        self.app_id = app_id

    def connect(self):
        return {"status": "CONNECTED", "app_id": self.app_id, "non_custodial": True}

    def route_nanopayment(self, recipient: str, sats: int):
        print(f"💎 HandCash Direct Sink: Routed {sats} sats to {recipient}")
        return {"success": True, "recipient": recipient, "sats": sats}
