import requests

class OllamaClient:
    def __init__(self, model="mistral"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        res = requests.post(self.url, json=payload, timeout=120)
        res.raise_for_status()
        return res.json()["response"]