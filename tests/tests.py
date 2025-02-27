# test_assistant.py
import pytest
from unittest.mock import MagicMock
from app.assistant import Assistant

@pytest.fixture
def mock_llm_service():
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_rag_service():
    mock = MagicMock()
    mock.query_engine.query.return_value.response = "Mocked response"
    return mock

@pytest.fixture
def assistant(mock_llm_service, mock_rag_service, monkeypatch):
    monkeypatch.setattr("app.assistant.LLMService", lambda x: mock_llm_service)
    monkeypatch.setattr("app.assistant.RAGService", lambda x, y: mock_rag_service)
    return Assistant("test_data")

def test_assistant_initialization(assistant):
    assert assistant.llm_service is not None
    assert assistant.rag is not None

def test_assistant_get_response(assistant, mock_rag_service):
    query = "Test query"
    response = assistant.getResponse(query)
    mock_rag_service.query_engine.query.assert_called_once()
    assert response == "Mocked response"

# test_doc_uploader.py
import pytest
import os
from app.doc_uploader import DocUploader

@pytest.fixture
def doc_uploader(tmp_path):
    upload_dir = tmp_path / "uploads"
    return DocUploader(upload_dir=str(upload_dir))

def test_doc_uploader_initialization(doc_uploader):
    assert os.path.exists(doc_uploader.upload_dir)

def test_doc_uploader_save_file(doc_uploader):
    file_content = b"Test file content"
    filename = "test.txt"
    file_path = doc_uploader.save_file(file_content, filename)
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        assert f.read() == file_content

def test_doc_uploader_delete_file(doc_uploader):
    file_content = b"Test file content"
    filename = "test.txt"
    file_path = doc_uploader.save_file(file_content, filename)
    result = doc_uploader.delete_file(filename)
    assert result is True
    assert not os.path.exists(file_path)

def test_doc_uploader_delete_nonexistent_file(doc_uploader):
    filename = "nonexistent.txt"
    result = doc_uploader.delete_file(filename)
    assert result is False

# test_llm_service.py
import pytest
from unittest.mock import patch, MagicMock
from app.llm_service import LLMService
import os

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test_key")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "test_endpoint")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "test_version")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT_NAME", "test_deployment")

@pytest.fixture
def llm_service(mock_env, tmp_path):
    config_path = tmp_path / "config.json"
    with open(config_path, "w") as f:
        f.write('{"model": "test_model", "embedding_model": "test_embed_model", "embedding_deployment": "test_embed_deployment"}')
    return LLMService(str(config_path))

def test_llm_service_initialization(llm_service):
    assert llm_service.llm is not None
    assert llm_service.embed_model is not None
    assert llm_service.config["model"] == "test_model"

# test_rag_service.py
import pytest
from unittest.mock import MagicMock, patch
from app.rag_service import RAGService
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

@pytest.fixture
def mock_llm_service():
    return MagicMock()

@pytest.fixture
def mock_documents():
    mock_doc = MagicMock()
    return [mock_doc]

@pytest.fixture
def rag_service(mock_llm_service, mock_documents, tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setattr(SimpleDirectoryReader, "load_data", lambda x: mock_documents)
    return RAGService(str(data_dir), mock_llm_service)

def test_rag_service_initialization(rag_service, mock_documents):
    assert rag_service.documents == mock_documents
    assert isinstance(rag_service.index, VectorStoreIndex)
    assert rag_service.query_engine is not None