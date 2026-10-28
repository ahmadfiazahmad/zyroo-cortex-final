"""Configuration — every secret comes from .env, nothing is hard-coded.

Copy .env.example to .env and paste your own keys there.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Cortex AI Backend API"
    # SQLite by default so the project runs anywhere with zero setup.
    # For production set e.g. postgresql://user:pass@host:5432/cortex
    database_url: str = "sqlite:///./cortex.db"

    jwt_secret: str = "change-me-in-production-use-a-long-random-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 day

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_pro: str = ""
    stripe_price_team: str = ""
    app_base_url: str = "http://localhost:8000"

    # Emails (comma-separated) that are made admin on registration.
    # Example: ADMIN_EMAILS=ahmad@example.com,mentor@zyroo.org
    admin_emails: str = ""

    max_upload_mb: int = 10
    chat_max_chars: int = 2000

    # Embeddings: "hash" = deterministic offline fallback (default, used
    # by the tests), "fastembed" = real neural embeddings
    # (sentence-transformers/all-MiniLM-L6-v2, 384 dims, via ONNX).
    # Set EMBEDDING_PROVIDER=fastembed in production for true semantic search.
    embedding_provider: str = "hash"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    @property
    def admin_email_set(self) -> set:
        return {e.strip().lower() for e in self.admin_emails.split(",") if e.strip()}


settings = Settings()
