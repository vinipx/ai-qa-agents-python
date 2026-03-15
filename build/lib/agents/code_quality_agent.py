from langchain_core.messages import SystemMessage
from core.telemetry import track_metrics
from core.state import AgentState

# Role: Code Quality Gate Agent (Reviewer)
# Goal: Run static analysis, linting, and code reviews. 
# Mandate: Guarantee high-quality code and compliance with PR mandates before any code is approved for Pull Request creation.
# Resources: Linting rules, code complexity thresholds.
CODE_QUALITY_PROMPT = """You are a Code Quality Reviewer. 
Analyze the generated automation code.
Perform static analysis and identify issues (linting, complexity, security vulnerabilities).
Your review acts as a final gate before the Pull Request is created.
"""

@track_metrics(agent_name="CodeQualityGate")
def code_quality_node(state: AgentState, config: dict):
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
