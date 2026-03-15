from langchain_core.messages import SystemMessage
from core.telemetry import track_metrics
from core.state import AgentState

from core.config import settings

# Role: Test Automation Engineer Agent (Builder)
# Goal: Write and maintain automated test scripts for Web, API, Mobile, etc.
# Mandate: All changes MUST be proposed via Pull Request (PR) only. Direct commits to main/protected branches are forbidden.
# Resources: Target Repository (e.g. GitHub)
AUTO_ENGINEER_PROMPT = """You are a Test Automation Engineer. 
Write automated tests based on the manual test cases and the architecture strategy.
Code should be robust, clean, and follow the Page Object Model if UI tests are needed.
Your work must be prepared as a new branch/commit ready for Pull Request (PR) review.
Target Repo: {repo_url}
"""

@track_metrics(agent_name="TestAutomationEngineer")
def test_auto_engineer_node(state: AgentState, config: dict):
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
