class QluxDatabase:
    def __init__(self):
        self.storage = {}

    def set(self, key: str, value: str):
        self.storage[key] = value
        return True

    def get(self, key: str):
        return self.storage.get(key, None)
