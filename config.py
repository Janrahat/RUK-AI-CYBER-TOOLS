"""Configuration loaded from environment variables or an optional .env file."""
import os
from dotenv import load_dotenv
load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_API_URL = os.getenv("AI_API_URL", "https://api.openai.com/v1/chat/completions").strip()
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini").strip()
HOST = os.getenv("RUK_HOST", "127.0.0.1")
PORT = int(os.getenv("RUK_PORT", "8080"))
SECRET_KEY = os.getenv("RUK_SECRET_KEY", "dev-only-change-me")
DATABASE = os.getenv("RUK_DATABASE", "ruk_analytics.sqlite3")
PUBLIC_BASE_URL = os.getenv("RUK_PUBLIC_BASE_URL", "").rstrip("/")
RETENTION_DAYS = max(1, int(os.getenv("RUK_RETENTION_DAYS", "30")))
