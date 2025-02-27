

from app.services.llm_service import LLMService
from app.services.rag_service import RAGService


class Assistant:

    def __init__(self, data_dir):
        self.llm_service = LLMService('config.json')
        self.rag = RAGService(data_dir,self.llm_service)


    def getResponse(self,query: str):
        answer = self.rag.query_engine.query(f"{query}.Give beautiful markdown text and also Give one or two emojis in output wherever seems necessary to make the response rich.")
        print(answer)
        return(answer.response)