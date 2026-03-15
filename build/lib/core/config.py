import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration for the framework. Model-agnostic setup.
    """
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai") # openai, google, anthropic
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY", None)
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY", None)
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY", None)
    
    # Requirement Tracking (e.g., JIRA)
    jira_url: str | None = os.getenv("JIRA_URL", None)
    jira_token: str | None = os.getenv("JIRA_TOKEN", None)
    
    # Repository Details (e.g., GitHub, GitLab, Bitbucket)
    repo_url: str | None = os.getenv("REPO_URL", None)
    repo_token: str | None = os.getenv("REPO_TOKEN", None)
    repo_provider: str = os.getenv("REPO_PROVIDER", "github") # github, gitlab, bitbucket
    
    # Langsmith Observability
    langchain_tracing_v2: str = os.getenv("LANGCHAIN_TRACING_V2", "true")
    langchain_api_key: str | None = os.getenv("LANGCHAIN_API_KEY", None)
    langchain_project: str = os.getenv("LANGCHAIN_PROJECT", "ai-qa-agents")

settings = Settings()
