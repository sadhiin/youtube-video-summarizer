# -*- coding: utf-8 -*-
"""
Module to get embedding models for vector operations.
"""

import os
from app.config import config
from app.utils.logger import logging

def initalize_embedding_model():
    """
    Get the embedding model for vector operations.

    Returns either NVIDIA embeddings if API key is available,
    or falls back to HuggingFaceEmbeddings.
    """
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")

    if nvidia_api_key:
        try:
            from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

            embedding_model = NVIDIAEmbeddings(
                model=config.VECTOR_EMBEDDING_MODEL,
                api_key=nvidia_api_key,
                truncate="NONE")

            logging.info("Using NVIDIA embeddings model")
            return embedding_model
        except Exception as e:
            logging.error(f"Error loading NVIDIA embeddings: {e}")
            logging.warning("Falling back to HuggingFace embeddings")

    # Fallback to HuggingFace embeddings
    try:
        from langchain.embeddings import HuggingFaceEmbeddings

        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embedding_model = HuggingFaceEmbeddings(model_name=model_name)

        logging.info(f"Using HuggingFace embeddings model: {model_name}")
        return embedding_model
    except Exception as e:
        logging.error(f"Error loading HuggingFace embeddings: {e}")
        logging.error("Falling back to 'Fake' embedding model")

        # Ultimate fallback - fake embeddings that return zeros
        # This is just to prevent hard crashes if no embedding model works
        from langchain.embeddings.base import Embeddings

        class FallbackEmbeddings(Embeddings):
            def embed_documents(self, texts):
                return [[0.0] * 384 for _ in texts]

            def embed_query(self, text):
                return [0.0] * 384

        logging.warning("WARNING: Using fallback embeddings (zeros) - chat functionality may not work properly")
        return FallbackEmbeddings()