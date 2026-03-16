from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from core.telemetry import async_track_metrics
from core.state import AgentState

# Role: Technical Writer Agent (Documenter)

@async_track_metrics(agent_name="TechnicalWriter")
async def tech_writer_node(state: AgentState, config: RunnableConfig | None = None):
    """
    Technical Writer Agent.
    Maintains project and framework documentation.
    """
    # In a real implementation, we would call LLM with TECH_WRITER_PROMPT
    documentation_updates = (
        "README.md: Updated with Pytest execution commands.\n"
        "TESTS.md: Created a list of automated test cases and coverage.\n"
        "API.md: Documented the endpoint structure for login API tests."
    )
    
    msg = SystemMessage(
        content=f"--- ROLE: Technical Writer ---\n"
                f"GOAL: Ensure all technical artifacts and tests are documented.\n"
                f"UPDATES:\n{documentation_updates}"
    )
    
    return {
        "messages": [msg],
        "sender": "TechnicalWriter"
    }
