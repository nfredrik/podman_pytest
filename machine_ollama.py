"""Module for streaming responses from the Ollama language model."""
from typing import Dict, Any, Generator, List, Optional, Tuple
import ollama
from ollama import ResponseError
import sys


def is_model_installed(model_name: str) -> bool:
    """Check if a specific Ollama model is installed.
    
    Args:
        model_name: Name of the model to check (e.g., 'llama3')
        
    Returns:
        bool: True if model is installed, False otherwise
    """
    try:
        ollama.show(model_name)
        return True
    except ResponseError:
        return False
    except Exception as e:
        print(f"Error checking model: {e}", file=sys.stderr)
        return False


def list_installed_models() -> List[Dict[str, Any]]:
    """List all installed Ollama models.
    
    Returns:
        List of dictionaries containing model information
    """
    try:
        models = ollama.list()
        return models.get('models', [])
    except Exception as e:
        print(f"Error listing models: {e}", file=sys.stderr)
        return []


def ensure_model_installed(model_name: str = 'llama3') -> bool:
    """Ensure the specified model is installed, offer to install if not.
    
    Args:
        model_name: Name of the model to check/install
        
    Returns:
        bool: True if model is available, False otherwise
    """
    if is_model_installed(model_name):
        return True
        
    print(f"Model '{model_name}' is not installed.")
    response = input(f"Would you like to install '{model_name}'? (y/n): ").strip().lower()
    
    if response == 'y':
        try:
            print(f"Downloading {model_name}... (this may take a while)")
            ollama.pull(model_name)
            return True
        except Exception as e:
            print(f"Error installing model: {e}", file=sys.stderr)
            return False
    return False


def stream_llm_response(prompt: str, model: str = 'llama3') -> Generator[str, None, None]:
    """Stream responses from the Ollama language model.
    
    Args:
        prompt: The input text to send to the model.
        model: The name of the Ollama model to use. Defaults to 'llama3'.
        
    Yields:
        str: Chunks of the generated response as they become available.
        
    Example:
        for chunk in stream_llm_response("Hello, how are you?"):
            print(chunk, end='', flush=True)
    """
    try:
        stream = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
                
    except Exception as e:
        yield f"\nError getting response from Ollama: {e}"


def main() -> None:
    """Demonstrate streaming LLM responses with model checking."""
    model_name = 'llama3'
    
    # Check if model is installed
    if not ensure_model_installed(model_name):
        print("Required model is not available. Exiting.", file=sys.stderr)
        return
        
    # List all installed models
    print("\nInstalled models:")
    for model in list_installed_models():
        print(f"- {model['model']} (size: {model.get('size', 'unknown')} bytes)")
    
    # Example prompts
    prompts = [
        'If I tell you my name will you remember it? 20 questions later or in another session?',
        'What is my name?',
        # Add more prompts as needed
    ]
    
    # Process each prompt
    for prompt in prompts:
        print(f"\n\nPrompt: {prompt}")
        print("-" * 50)
        try:
            for chunk in stream_llm_response(prompt=prompt, model=model_name):
                print(chunk, end='', flush=True)
        except Exception as e:
            print(f"\nError during generation: {e}", file=sys.stderr)
    
    print("\n\nDone!")


if __name__ == "__main__":
    main()
