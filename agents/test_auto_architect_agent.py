from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from core.telemetry import async_track_metrics
from core.state import AgentState

# Role: Test Automation Architect Agent

@async_track_metrics(agent_name="TestAutomationArchitect")
async def test_auto_architect_node(state: AgentState, config: RunnableConfig | None = None):
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
