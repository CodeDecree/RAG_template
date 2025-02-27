from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from app.services.llm_service import LLMService

class RAGService:

    def __init__(self, data_dir, LLMService: LLMService):
        
        self.documents = SimpleDirectoryReader(
        input_dir=data_dir
        ).load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)

        self.query_engine = self.index.as_query_engine()

