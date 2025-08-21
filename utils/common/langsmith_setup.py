"""
LangSmith configuration utility for safe initialization
"""
import os
from typing import Optional
from configs.constants import LANGSMITH_TRACING, LANGSMITH_API_KEY, LANGSMITH_PROJECT, LANGSMITH_ENDPOINT

def setup_langsmith() -> bool:
    """
    Safely initialize LangSmith tracing if configured.
    Returns True if LangSmith is successfully initialized, False otherwise.
    """
    try:
        if not LANGSMITH_TRACING:
            print("[LANGSMITH] Tracing disabled - skipping initialization")
            return False
            
        if not LANGSMITH_API_KEY:
            print("[LANGSMITH] No API key provided - skipping initialization")
            return False
            
        # Set environment variables for LangSmith
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
        os.environ["LANGCHAIN_ENDPOINT"] = LANGSMITH_ENDPOINT
        
        print(f"[LANGSMITH] Successfully initialized for project: {LANGSMITH_PROJECT}")
        return True
        
    except Exception as e:
        print(f"[LANGSMITH] Failed to initialize: {e}")
        return False

def get_langsmith_config() -> dict:
    """
    Get current LangSmith configuration status
    """
    return {
        "tracing_enabled": LANGSMITH_TRACING,
        "api_key_configured": bool(LANGSMITH_API_KEY),
        "project": LANGSMITH_PROJECT,
        "endpoint": LANGSMITH_ENDPOINT
    }
