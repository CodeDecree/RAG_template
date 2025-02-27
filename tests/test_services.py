import os
import json
import tempfile
import pytest

from app.services.doc_uploader import DocUploader
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.assistant import Assistant

# ---------------------------
# Test for DocUploader
# ---------------------------
def test_doc_uploader_save_and_delete(tmp_path):
    # Use pytest's temporary directory
    upload_dir = tmp_path / "uploads"
    uploader = DocUploader(upload_dir=str(upload_dir))
    
    # Test saving a file
    file_content = b"Hello, world!"
    filename = "test.txt"
    file_path = uploader.save_file(file_content, filename)
    
    # Verify file exists and content is correct
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        content = f.read()
    assert content == file_content
    
    # Test file deletion
    deleted = uploader.delete_file(filename)
    assert deleted is True
    assert not os.path.exists(file_path)

# ---------------------------
# Fixtures for LLMService and environment
# ---------------------------
@pytest.fixture
def dummy_config(tmp_path):
    # Create a dummy configuration file for LLMService
    config = {
        "model": "dummy-model",
        "temperature": 0.5,
        "max_retries": 1,
        "embedding_model": "dummy-embed",
        "embedding_deployment": "dummy-deployment"
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config))
    return str(config_file)

@pytest.fixture(autouse=True)
def set_dummy_env(monkeypatch):
    # Set dummy environment variables needed by LLMService
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT_NAME", "dummy-deployment-name")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "dummy-api-key")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "http://dummy-endpoint")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "dummy-version")

# ---------------------------
# Test for LLMService
# ---------------------------
# def test_llm_service_initialization(dummy_config):
#     service = LLMService(config_path=dummy_config)
#     assert service.llm is not None
#     assert service.embed_model is not None

# ---------------------------
# Test for RAGService
# ---------------------------
# def test_rag_service_initialization(tmp_path, dummy_config):
#     # Create a dummy data directory with a sample text file
#     data_dir = tmp_path / "data"
#     data_dir.mkdir()
#     sample_file = data_dir / "sample.txt"
#     sample_file.write_text("This is a test document.")
    
#     # Initialize a dummy LLMService instance
#     llm_service = LLMService(config_path=dummy_config)
    
#     # Create RAGService instance
#     rag_service = RAGService(data_dir=str(data_dir), LLMService=llm_service)
    
#     # Check that documents were loaded and a query engine exists
#     assert len(rag_service.documents) > 0
#     assert hasattr(rag_service, "query_engine")

# ---------------------------
# Test for Assistant getResponse
# ---------------------------
# def test_assistant_get_response(tmp_path, dummy_config):
#     # Create a dummy data directory with sample content
#     data_dir = tmp_path / "data"
#     data_dir.mkdir()
#     (data_dir / "sample.txt").write_text("Dummy content for testing.")
    
#     # Create an Assistant instance
#     assistant = Assistant(data_dir=str(data_dir))
    
#     # Monkeypatch the query method of rag.query_engine to return a dummy response
#     dummy_response = type("DummyResponse", (), {"response": "Test response 😊"})()
#     assistant.rag.query_engine.query = lambda query: dummy_response
    
#     result = assistant.getResponse("Who is the author?")
#     assert result == "Test response 😊"
