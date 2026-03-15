from core.config import settings
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm() -> BaseChatModel:
    """
    Factory to return a LangChain ChatModel based on configuration.
    Supports OpenAI, Anthropic, and Ollama (Local).
    """
    provider = settings.llm_provider.lower()
    model = settings.model_name
    
    if provider == "openai":
        return ChatOpenAI(model=model, api_key=settings.openai_api_key)
    elif provider == "anthropic":
        return ChatAnthropic(model=model, api_key=settings.anthropic_api_key)
    elif provider == "ollama":
        # Ollama usually runs at http://localhost:11434 by default
        return ChatOllama(model=model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
