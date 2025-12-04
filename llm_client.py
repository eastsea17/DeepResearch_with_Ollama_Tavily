import requests
import json
from config import LLMConfig

class OllamaClient:
    def __init__(self, model_name=None):
        self.base_url = LLMConfig.BASE_URL
        self.model = model_name if model_name else LLMConfig.MODEL_NAME
        self.temperature = LLMConfig.TEMPERATURE
        self.context_window = LLMConfig.CONTEXT_WINDOW

    def generate(self, prompt, system_prompt=None):
        """
        Generate a response from the Ollama model.
        
        Args:
            prompt (str): The user prompt.
            system_prompt (str, optional): The system prompt.
            
        Returns:
            str: The generated text.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_ctx": self.context_window
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return f"Error: {str(e)}"

if __name__ == "__main__":
    client = OllamaClient()
    print(f"OllamaClient initialized for model: {client.model}")
