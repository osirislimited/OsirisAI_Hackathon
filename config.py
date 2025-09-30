"""
Configuration file for Osiris.AI
Store your API keys and settings here
"""

import os

# Try to load dotenv if available, otherwise use environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, will use os.getenv with defaults
    pass

class Config:
    """Configuration class for API keys and settings"""
    
    # *** CHANGE YOUR API KEYS HERE ***
    
    # Gemini API Key - Get from: https://makersuite.google.com/app/apikey
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDA-xVqq5eZ9u8kIkbaXDnFuXC6JxtBIhQ")
    
    # Google Speech API Key (optional - uses free tier by default)
    GOOGLE_SPEECH_API_KEY = os.getenv("GOOGLE_SPEECH_API_KEY", "")
    
    # Application settings
    APP_NAME = "Osiris.AI"
    APP_VERSION = "1.0.0"
    
    # Voice settings
    VOICE_LANGUAGE_CANTONESE = "zh-HK"
    VOICE_LANGUAGE_ENGLISH = "en-US"
    TTS_RATE = 150
    TTS_VOLUME = 0.9
    
    # Camera settings
    CAMERA_INDEX = 0
    IMAGE_QUALITY = 95
    
    # Gemini model settings
    GEMINI_MODEL = "gemini-2.0-flash-exp"
    
    # File paths
    RESULTS_DIR = "results"
    LOGS_DIR = "logs"
    
    @classmethod
    def validate_config(cls):
        """Validate configuration"""
        issues = []
        
        if cls.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            issues.append("❌ Gemini API key not configured")
        
        # Create directories if they don't exist
        os.makedirs(cls.RESULTS_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        
        return issues

# Global config instance
config = Config()