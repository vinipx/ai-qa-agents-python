from langchain_core.messages import SystemMessage
from core.telemetry import track_metrics
from core.state import AgentState

# Role: Test Automation Architect Agent
# Goal: Designs the Test Automation Framework (TAF) from scratch or proposes strategy/governance for an existing one.
# Resources: Framework best practices, reporting, and CI/CD pipelines.
AUTO_ARCHITECT_PROMPT = """You are a Test Automation Architect. 
Analyze the current requirements and manual test cases.
Propose a Test Automation Framework (TAF) strategy including Tools, Reporting, Governance, and CI/CD integration.
"""

@track_metrics(agent_name="TestAutomationArchitect")
def test_auto_architect_node(state: AgentState, config: dict):
    """
    Test Automation Architect Agent.
    Designs frameworks, strategies, and reporting structures.
    """
    # In a real implementation, we would call LLM with AUTO_ARCHITECT_PROMPT
    strategy = (
        "Strategy: Use Python/Pytest with Playwright for Web UI tests.\n"
        "API Testing: Pytest + Requests.\n"
        "Reporting: Allure for detailed HTML reports.\n"
        "Governance: Modular design, Page Object Model (POM).\n"
        "CI/CD: GitHub Actions pipeline for regression."
    )
    
    msg = SystemMessage(
        content=f"--- ROLE: Test Automation Architect ---\n"
                f"GOAL: Design big-picture automation strategy and framework capabilities.\n"
                f"STRATEGY:\n{strategy}"
    )
    
    return {
        "messages": [msg],
        "sender": "TestAutomationArchitect"
    }
