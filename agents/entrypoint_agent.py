from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from core.telemetry import track_metrics
from core.state import AgentState

# Role: SDLC Architect & Orchestrator

@track_metrics(agent_name="Supervisor")
def entrypoint_node(state: AgentState, config: RunnableConfig | None = None):
    """
    Entrypoint / Architect Agent (Supervisor).
    Orchestrates tasks, plans execution, and requires Human-in-the-Loop.
    """
    messages = state.get("messages", [])
    last_message = messages[-1].content if messages else ""
    
    # Simple logic to determine if we need a plan
    if not state.get("plan"):
        # Real LLM call example (commented out to preserve your mock flow, 
        # but ready to be enabled):
        # llm = get_llm()
        # prompt = ChatPromptTemplate.from_template(SUPERVISOR_PROMPT)
        # chain = prompt | llm
        # result = chain.invoke({"requirement": last_message, "plan": ""})
        
        plan_content = (
            "1. Manual QA Expert: Create comprehensive test cases from requirements.\n"
            "2. Test Auto Architect: Design the framework strategy and reporting structure.\n"
            "3. Test Automation Engineer: Implement automated scripts in the target repository.\n"
            "4. Code Quality Gate: Perform static analysis and review automation code.\n"
            "5. Technical Writer: Update project documentation and README."
        )
        
        msg = SystemMessage(
            content=f"--- SUPERVISOR ROLE: SDLC Architect ---\n"
                    f"GOAL: Orchestrate QE lifecycle for: '{last_message}'\n\n"
                    f"PROPOSED PLAN:\n{plan_content}\n\n"
                    "Waiting for user approval (HITL)..."
        )
        
        return {
            "messages": [msg],
            "plan": plan_content,
            "approved": False,
            "next_agent": None,
            "sender": "Supervisor"
        }
    
    # Sequence of agents to visit
    agent_sequence = [
        "ManualQAExpert",
        "TestAutomationArchitect",
        "TestAutomationEngineer",
        "CodeQualityGate",
        "TechnicalWriter"
    ]
    
    # If approved and need to route
    if state.get("approved"):
        current_sender = state.get("sender")
        
        if current_sender == "Supervisor" or current_sender == "User":
            next_step = agent_sequence[0]
            msg = SystemMessage(content=f"Plan approved. Routing to {next_step}.")
            return {
                "messages": [msg],
                "next_agent": next_step,
                "sender": "Supervisor"
            }
        
        # Determine who is next in the sequence
        try:
            current_index = agent_sequence.index(current_sender)
            if current_index < len(agent_sequence) - 1:
                next_step = agent_sequence[current_index + 1]
                msg = SystemMessage(content=f"{current_sender} finished. Routing to {next_step}.")
                return {
                    "messages": [msg],
                    "next_agent": next_step,
                    "sender": "Supervisor"
                }
            else:
                msg = SystemMessage(content="All agents finished. Preparing to raise PR.")
                return {
                    "messages": [msg],
                    "next_agent": "FINISH",
                    "sender": "Supervisor"
                }
        except ValueError:
            # If current_sender is not in agent_sequence (e.g. first time after approval)
            next_step = agent_sequence[0]
            msg = SystemMessage(content=f"Routing to {next_step}.")
            return {
                "messages": [msg],
                "next_agent": next_step,
                "sender": "Supervisor"
            }
            
    return {"messages": [], "sender": "Supervisor"}
