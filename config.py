import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TavilyConfig:
    API_KEY = os.getenv("TAVILY_API_KEY")
    BASE_URL = "https://api.tavily.com/search"
    
    # User-configurable parameters
    SEARCH_DEPTH = "advanced"  # "basic" or "advanced"
    MAX_RESULTS = 10
    INCLUDE_DOMAINS = []
    EXCLUDE_DOMAINS = []
    
    # Advanced parameters
    INCLUDE_ANSWER = True
    INCLUDE_RAW_CONTENT = False
    INCLUDE_IMAGES = False

class LLMConfig:
    # Available Models
    MODEL_LOCAL = "deepseek-r1:8b"
    MODEL_DEEPSEEK_CLOUD = "deepseek-v3.1:671b-cloud"
    MODEL_GPT_OSS_CLOUD = "gpt-oss:120b-cloud"

    # Default Configuration
    MODEL_NAME = MODEL_DEEPSEEK_CLOUD
    BASE_URL = "http://localhost:11434/api/generate"
    TEMPERATURE = 0.6
    CONTEXT_WINDOW = 8192

class ReportConfig:
    RESULTS_DIR = "results"
