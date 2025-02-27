import json
import os
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from dotenv import load_dotenv
from llama_index.core import Settings


load_dotenv()

class LLMService:

    def __init__(self,config_path='config.json'):

        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.llm = AzureOpenAI(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
            model=self.config.get("model", "gpt-4o"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=self.config.get("temperature", 0.3),
            max_tokens=2000,
            max_retries=self.config.get("max_retries", 3),
        )
        Settings.llm = self.llm

        self.embed_model = AzureOpenAIEmbedding(
            model=self.config.get("embedding_model", "text-embedding-ada-002"),
            deployment_name=self.config.get("embedding_deployment", "text-embedding-ada-002"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        Settings.embed_model = self.embed_model

        print('voila llmservice')

