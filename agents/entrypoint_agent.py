from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from core.telemetry import async_track_metrics
from core.state import AgentState
import logging

logger = logging.getLogger("QORE_SUPERVISOR")

# Role: SDLC Architect & Orchestrator

@async_track_metrics(agent_name="Supervisor")
async def entrypoint_node(state: AgentState, config: RunnableConfig | None = None):
    """
    Entrypoint / Architect Agent (Supervisor).
    Orchestrates tasks, plans execution, and requires Human-in-the-Loop.
    """
    messages = state.get("messages", [])
    last_message = messages[-1].content if messages else ""
    approved = state.get("approved", False)
    current_sender = state.get("sender", "User")
    
    logger.info(f"--- Supervisor Entry ---")
    logger.info(f"Sender: {current_sender} | Approved: {approved} | Has Plan: {bool(state.get('plan'))}")

    # 1. PLAN GENERATION PHASE
    if not state.get("plan"):
        logger.info("Generating new plan...")
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
            "approved": False, # Stop for HITL
            "next_agent": None,
            "sender": "Supervisor"
        }
    
    # 2. ROUTING PHASE (After Plan is created)
    agent_sequence = [
        "ManualQAExpert",
        "TestAutomationArchitect",
        "TestAutomationEngineer",
        "CodeQualityGate",
        "TechnicalWriter"
    ]
    
    if approved:
        # If it's the first time after approval, or coming from Supervisor/User, start the sequence
        if current_sender in ["Supervisor", "User"]:
            next_step = agent_sequence[0]
            logger.info(f"Plan is approved. Starting sequence at: {next_step}")
            msg = SystemMessage(content=f"Sequence initiated. Handing over to {next_step}.")
            return {
                "messages": [msg],
                "next_agent": next_step,
                "sender": "Supervisor"
            }
        
        # Otherwise, find where we are in the sequence and move to next
        try:
            current_index = agent_sequence.index(current_sender)
            if current_index < len(agent_sequence) - 1:
                next_step = agent_sequence[current_index + 1]
                logger.info(f"Worker {current_sender} finished. Routing to next: {next_step}")
                msg = SystemMessage(content=f"{current_sender} task verified. Proceeding to {next_step}.")
                return {
                    "messages": [msg],
                    "next_agent": next_step,
                    "sender": "Supervisor"
                }
            else:
                logger.info("All agents in sequence finished.")
                msg = SystemMessage(content="Orchestration complete. All quality gates passed. Finalizing artifacts.")
                return {
                    "messages": [msg],
                    "next_agent": "FINISH",
                    "sender": "Supervisor"
                }
        except ValueError:
            # Fallback if sender is unknown
            next_step = agent_sequence[0]
            logger.info(f"Sender {current_sender} unknown. Defaulting to first step: {next_step}")
            return {
                "messages": [SystemMessage(content=f"Routing to {next_step}.")],
                "next_agent": next_step,
                "sender": "Supervisor"
            }
            
    logger.info("Supervisor standby: Waiting for approval flag.")
    return {"messages": [], "sender": "Supervisor"}
