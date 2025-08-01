from ..LLMInterface import LLMInterface
from ..LLMEnums import GeminiEnums
import logging
from typing import Optional
import requests

class OllamaProvider(LLMInterface):
    def __init__(self,api_url:str,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None  
        self.embedding_size = None

        self.logger = logging.getLogger(__name__)
    
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        
        if not self.api_url:
            self.logger.error("Url for Ollama not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model for Ollama was not set")
            return None
        
        return None

    def embed_text(self, text: str, document_type: str = None):
        
        if not self.api_url:
            self.logger.error("Url for Ollama not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Ollama was not set")
            return None
        
        data = {
            "model": self.embedding_model_id,
            "prompt": text
        }
        try:
            # Generate embeddings
            response = requests.post(self.api_url + "/api/embeddings", json=data)
            json_response = response.json()
            embedding = json_response.get("embedding")

            if not embedding:
                self.logger.error("No embedding found in the response from Ollama")
                return None
            return embedding
        except requests.RequestException as e:
            self.logger.error(f"Embedding request failed: {str(e)}")
            return None
        except ValueError:
            self.logger.error("Failed to decode JSON from Ollama response")
            return None

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "parts": [{"text": self.process_text(prompt)}]
        }
