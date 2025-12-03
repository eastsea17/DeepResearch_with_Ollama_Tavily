import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TavilyConfig:
    API_KEY = os.getenv("TAVILY_API_KEY")
    BASE_URL = "https://api.tavily.com/search"
    
    # User-configurable parameters
    SEARCH_DEPTH = "basic"  # "basic" or "advanced"
    MAX_RESULTS = 5
    INCLUDE_DOMAINS = []
    EXCLUDE_DOMAINS = []
    
    # Advanced parameters
    INCLUDE_ANSWER = True
    INCLUDE_RAW_CONTENT = False
    INCLUDE_IMAGES = False

class LLMConfig:
    MODEL_NAME = "deepseek-r1:8b"
    BASE_URL = "http://localhost:11434/api/generate"
    TEMPERATURE = 0.6
    CONTEXT_WINDOW = 8192

class ReportConfig:
    RESULTS_DIR = "results"
