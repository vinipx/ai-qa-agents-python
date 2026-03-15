from langchain_core.messages import SystemMessage
from core.telemetry import track_metrics
from core.state import AgentState

from core.config import settings

# Role: Manual QA Expert Agent
# Goal: Receives requirements (User Stories, Features, FRDs) and creates comprehensive manual test cases.
# Resources: Requirement tracking (e.g. JIRA)
MANUAL_QA_PROMPT = """You are a Manual QA Specialist. 
Analyze the requirement: {requirement}
Generate comprehensive test cases (Functional and Non-Functional).
Reference JIRA Source: {jira_url}
"""

from langchain_core.runnables import RunnableConfig

@track_metrics(agent_name="ManualQAExpert")
def manual_qa_node(state: AgentState, config: RunnableConfig | None = None):
    """
    Manual QA Expert Agent.
    Creates, updates, and maintains comprehensive manual test cases.
    """
    jira_info = f"[Source: {settings.jira_url}]" if settings.jira_url else "[Source: No JIRA Configured]"
    
    # In a real implementation, we would call LLM with MANUAL_QA_PROMPT
    test_cases = (
        "TC01: Verify login with valid credentials (Functional)\n"
        "TC02: Verify login with invalid credentials (Functional/Security)\n"
        "TC03: Verify 'Forgot Password' functionality (Functional)\n"
        "TC04: Verify login response time is < 500ms (Non-Functional/Performance)"
    )
    
    msg = SystemMessage(
        content=f"--- ROLE: Manual QA Expert ---\n"
                f"GOAL: Create manual test cases for requirements.\n"
                f"SOURCE: {jira_info}\n\n"
                f"TEST CASES:\n{test_cases}"
    )
    
    return {
        "messages": [msg],
        "sender": "ManualQAExpert"
    }
