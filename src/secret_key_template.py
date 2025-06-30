"""
Secret Key Template for NDLens
Copy this file to secret_key.py and add your actual API key
"""

import os

# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys

# For deployment: reads from environment variable
# For local development: set directly
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Example for local development:
# OPENAI_API_KEY = "sk-proj-abcd1234..."
