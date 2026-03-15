from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from core.telemetry import track_metrics
from core.state import AgentState

from core.config import settings

# Role: Test Automation Engineer Agent (Builder)

@track_metrics(agent_name="TestAutomationEngineer")
def test_auto_engineer_node(state: AgentState, config: RunnableConfig | None = None):
    """
    Test Automation Engineer Agent.
    Writes and maintains automated test scripts based on the plan.
    """
    repo_info = f"[Target: {settings.repo_provider} @ {settings.repo_url}]" if settings.repo_url else "[Target: Local Filesystem]"
    
    # In a real implementation, we would call LLM with AUTO_ENGINEER_PROMPT
    test_code = (
        "import requests\n"
        "import pytest\n\n"
        "def test_api_status():\n"
        "    res = requests.get('https://api.example.com/status')\n"
        "    assert res.status_code == 200"
    )
    
    msg = SystemMessage(
        content=f"--- ROLE: Test Automation Engineer ---\n"
                f"GOAL: Implement automated tests based on architecture and manual TC.\n"
                f"TARGET: {repo_info}\n\n"
                f"GENERATED CODE:\n{test_code}"
    )
    
    return {
        "messages": [msg],
        "sender": "TestAutomationEngineer"
        # Note: We don't set next_agent; we return control to Supervisor
    }
