import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
PICKER_MODEL = os.getenv("PICKER_MODEL", "qwen3:1.7b")
ESCALATION_MODEL = os.getenv("ESCALATION_MODEL", "llama3.2:3b")
SHORTLIST_SIZE = 35
CONFIDENCE_THRESHOLD = 0.65
