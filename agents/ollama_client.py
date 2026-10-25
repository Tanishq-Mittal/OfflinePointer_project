import requests
from config import OLLAMA_HOST

def chat(model: str, prompt: str) -> tuple[str, float, float]:
    response = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": False,
            "options": {"temperature": 0, "seed": 7, "num_predict": 180}
        },
        timeout=90,
    )
    response.raise_for_status()
    data = response.json()
    message = data.get("message", {}).get("content", "")
    eval_count = data.get("eval_count", 0)
    eval_duration = data.get("eval_duration", 0) / 1_000_000_000
    tps = eval_count / eval_duration if eval_duration > 0 else 0
    return message, tps, float(data.get("total_duration", 0)) / 1_000_000
