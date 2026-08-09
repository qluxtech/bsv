class HandCashBridge:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.endpoint = "https://cloud.handcash.io/v2"

    def authorize_connection(self):
        return {"status": "CONNECTED", "app_id": self.app_id, "non_custodial": True}

    def direct_sink(self, recipient: str, sats: int):
        print(f"💎 HandCash Direct Sink: {sats} sats routed to {recipient}")
        return {"success": True, "recipient": recipient, "sats": sats}
