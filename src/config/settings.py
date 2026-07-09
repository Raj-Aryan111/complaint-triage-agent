"""
Project Configuration

Loads all environment variables from the .env file.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central configuration for the Complaint Triage Agent.
    """

    # ==========================================================
    # LLM
    # ==========================================================

    LLM_PROVIDER = os.getenv(
        "LLM_PROVIDER",
        "gemini",
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
    )

    MODEL_NAME = "gemini-2.5-flash"

    TEMPERATURE = 0.0

    MAX_TOKENS = 1000

    # ==========================================================
    # Database
    # ==========================================================

    DATABASE_URL = "sqlite:///database/complaints.db"

    # ==========================================================
    # Chroma Vector Database
    # ==========================================================

    CHROMA_DB_PATH = "vectorstore"

    # ==========================================================
    # Embedding Model
    # ==========================================================

    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

    # ==========================================================
    # RAG
    # ==========================================================

    TOP_K_POLICY = 3

    TOP_K_PRECEDENTS = 3

    # ==========================================================
    # Workflow
    # ==========================================================

    MAX_REVISIONS = 2

    CONFIDENCE_THRESHOLD = 0.80

    # ==========================================================
    # Development
    # ==========================================================

    DEV_MODE = True


# ==========================================================
# Singleton Settings Object
# ==========================================================

settings = Settings()