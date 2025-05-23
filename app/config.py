"""
Configuration settings for the YouTube summarizer application.
"""

import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class Config:
    """Base configuration class."""

    # Application info
    APP_NAME = "YouTube Video Summarizer"
    APP_VERSION = "0.1.2"

    ## Data directories
    DATA_DIR = Path("data")
    DOWNLOADS_DIR = DATA_DIR / "downloads"
    TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
    SUMMARIES_DIR = DATA_DIR / "summaries"
    REDIS_URL = os.getenv("REDIS_URL", None)
    # API keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TEMPERATURE = 0.3

    # Default models
    DEFAULT_TRANSCRIPTION_MODEL = "whisper-large-v3-turbo"
    DEFAULT_SUMMARY_MODEL = "llama-3.3-70b-versatile"
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "huggingface")
    VECTOR_EMBEDDING_MODEL = os.getenv("VECTOR_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", 5))
    RETRIEVAL_FETCH_K = int(os.getenv("RETRIEVAL_FETCH_K", 10))
    # os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    # os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
    # os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "YouTube Summarizer Project")
    PUBLIC_URL = os.getenv("PUBLIC_URL", "http://localhost:8000")
    
    ## chat related settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    
    # Vector store settings
    EMERGENCY_CHUNK_LIMIT = 9000
    SIMILARITY_THRESHOLD = 0.2
    
    # Retry configuration
    VECTOR_STORE_RETRIES = 3
    VECTOR_STORE_RETRY_DELAY = 1
    VECTOR_STORE_BACKOFF = 2

    MAX_CONTEXT_LENGTH = 4096
    
    @classmethod
    def initialize(cls):
        """Initialize the application configuration."""
        cls.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
        cls.TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

        # Validate required environment variables
        if not cls.GROQ_API_KEY:
            print("WARNING: GROQ_API_KEY environment variable not set.")
            print("Please set it in the .env file or environment variables.")

    @classmethod
    def get_paths(cls) -> Dict[str, Path]:
        """Get all application paths."""
        
        return {
            "data_dir": cls.DATA_DIR,
            "downloads_dir": cls.DOWNLOADS_DIR,
            "transcripts_dir": cls.TRANSCRIPTS_DIR,
            "summaries_dir": cls.SUMMARIES_DIR
        }

class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    LOG_LEVEL = "INFO"


# Determine which configuration to use based on environment
def get_config():
    """Get the appropriate configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "your_langsmith_api_key")
    os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
    os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "YouTube Summarizer Project")
    if env == "production":
        return ProductionConfig
    else:
        return DevelopmentConfig


# Create a config instance
config = get_config()
config.initialize()
