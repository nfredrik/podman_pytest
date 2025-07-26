"""Advanced LLM testing with pytest and mocks."""
import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, Optional


class MockLLM:
    """A mock LLM class for testing purposes."""
    
    def __init__(self, model_name: str = "mock-model"):
        self.model_name = model_name
        self.history = []
    
    def generate(
        self, 
        prompt: str, 
        temperature: float = 0.7,
        max_tokens: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a mock response based on the input prompt."""
        self.history.append({"prompt": prompt, "temperature": temperature, **kwargs})
        
        # Simple response logic based on input
        if "hello" in prompt.lower():
            return {"text": "Hello! How can I assist you today?", "tokens_used": 10}
        elif "joke" in prompt.lower():
            return {"text": "Why don't scientists trust atoms? Because they make up everything!", "tokens_used": 15}
        else:
            return {"text": "I'm not sure how to respond to that.", "tokens_used": 8}


# Fixture to provide a mock LLM instance
@pytest.fixture
def mock_llm():
    """Fixture that provides a mock LLM instance."""
    return MockLLM()


def test_llm_greeting(mock_llm):
    """Test that the LLM responds to greetings appropriately."""
    # Act
    response = mock_llm.generate("Hello, how are you?")
    
    # Assert
    assert "Hello" in response["text"]
    assert response["tokens_used"] > 0
    assert len(mock_llm.history) == 1


def test_llm_joke(mock_llm):
    """Test that the LLM can tell a joke."""
    # Act
    response = mock_llm.generate("Tell me a joke", temperature=0.9)
    
    # Assert
    assert "?" in response["text"]  # Jokes often end with a question mark
    assert mock_llm.history[0]["temperature"] == 0.9


def test_llm_unknown_prompt(mock_llm):
    """Test the LLM's response to an unknown prompt."""
    # Act
    response = mock_llm.generate("Random gibberish")
    
    # Assert
    assert "not sure" in response["text"].lower()


@patch.object(MockLLM, 'generate')
def test_llm_error_handling(mock_generate):
    """Test error handling in the LLM."""
    # Arrange
    mock_generate.side_effect = Exception("API Error")
    llm = MockLLM()
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        llm.generate("Test prompt")
    assert "API Error" in str(exc_info.value)


# Parametrized test for different inputs
@pytest.mark.parametrize("prompt, expected_keyword", [
    ("Say hi", "Hello"),
    ("Tell me a joke", "?"),
    ("Random text", "not sure"),
])
def test_llm_responses(mock_llm, prompt: str, expected_keyword: str):
    """Test multiple LLM responses with different inputs."""
    # Act
    response = mock_llm.generate(prompt)
    
    # Assert
    assert expected_keyword.lower() in response["text"].lower()