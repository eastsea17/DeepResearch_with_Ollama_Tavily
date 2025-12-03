import requests
import json
from config import TavilyConfig

class TavilyClient:
    def __init__(self):
        self.api_key = TavilyConfig.API_KEY
        self.base_url = TavilyConfig.BASE_URL
        
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables.")

    def search(self, query, **kwargs):
        """
        Perform a search using the Tavily API.
        
        Args:
            query (str): The search query.
            **kwargs: Override default configuration parameters.
        
        Returns:
            dict: The search results.
        """
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": kwargs.get("search_depth", TavilyConfig.SEARCH_DEPTH),
            "max_results": kwargs.get("max_results", TavilyConfig.MAX_RESULTS),
            "include_domains": kwargs.get("include_domains", TavilyConfig.INCLUDE_DOMAINS),
            "exclude_domains": kwargs.get("exclude_domains", TavilyConfig.EXCLUDE_DOMAINS),
            "include_answer": kwargs.get("include_answer", TavilyConfig.INCLUDE_ANSWER),
            "include_raw_content": kwargs.get("include_raw_content", TavilyConfig.INCLUDE_RAW_CONTENT),
            "include_images": kwargs.get("include_images", TavilyConfig.INCLUDE_IMAGES),
        }
        
        # Remove empty lists to avoid API issues if any
        if not payload["include_domains"]:
            del payload["include_domains"]
        if not payload["exclude_domains"]:
            del payload["exclude_domains"]

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching Tavily: {e}")
            return {"results": [], "error": str(e)}

if __name__ == "__main__":
    # Simple test
    try:
        client = TavilyClient()
        print("TavilyClient initialized successfully.")
    except ValueError as e:
        print(f"Initialization failed: {e}")
