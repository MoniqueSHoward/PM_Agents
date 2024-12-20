from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
import os
from openai import OpenAI

class Configuration:
    """Configuration management for the PM Agents system"""
    
    # File processing configurations
    MAX_AUDIO_DURATION = 60 * 60  # 60 minutes
    MAX_TEXT_WORDS = 10000
    SUPPORTED_AUDIO_FORMATS = {'.mp3', '.wav', '.m4a', '.wma'}
    SUPPORTED_TEXT_FORMATS = {'.txt', '.md', '.doc', '.docx'}
    
    # Model configurations
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 0.1
    DEFAULT_TIMEOUT = 300
    DEFAULT_MAX_RETRIES = 3

def load_environment():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    
    # Validate required environment variables
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def get_openai_api_key() -> str:
    """Get OpenAI API key from environment variables"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return api_key

def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with API key from environment"""
    api_key = get_openai_api_key()
    return OpenAI(api_key=api_key)

def get_default_llm_config() -> Dict:
    """Get default LLM configuration"""
    return {
        "config_list": [{
            "model": Configuration.DEFAULT_MODEL,
            "client": get_openai_client(),
            "api_key": get_openai_api_key(),
        }],
        "temperature": Configuration.DEFAULT_TEMPERATURE,
        "timeout": Configuration.DEFAULT_TIMEOUT,
        "max_retries": Configuration.DEFAULT_MAX_RETRIES
    }