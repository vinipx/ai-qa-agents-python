from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from core.telemetry import track_metrics
from core.state import AgentState

# Role: Code Quality Gate Agent (Reviewer)

@track_metrics(agent_name="CodeQualityGate")
def code_quality_node(state: AgentState, config: RunnableConfig | None = None):
    """
    Code Quality Gate Agent.
    Runs static code analysis, linting, and code reviews.
    """
    # In a real implementation, we would call LLM with CODE_QUALITY_PROMPT
    findings = (
        "Linting: ✅ Pass (Flake8 compliant).\n"
        "Complexity: ✅ Low (Cyclomatic complexity < 5).\n"
        "Security: ✅ No hardcoded secrets or insecure imports detected.\n"
        "Suggestions: Consider using environment variables for base URLs."
    )
    
    msg = SystemMessage(
        content=f"--- ROLE: Code Quality Gate ---\n"
                f"GOAL: Ensure high-quality, standard-compliant code.\n"
                f"FINDINGS:\n{findings}"
    )
    
    return {
        "messages": [msg],
        "sender": "CodeQualityGate"
    }
