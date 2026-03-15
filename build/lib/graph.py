from langgraph.graph import StateGraph, END
from core.state import AgentState
from agents.entrypoint_agent import entrypoint_node
from agents.test_auto_engineer_agent import test_auto_engineer_node
from agents.manual_qa_agent import manual_qa_node
from agents.test_auto_architect_agent import test_auto_architect_node
from agents.code_quality_agent import code_quality_node
from agents.tech_writer_agent import tech_writer_node

def route(state: AgentState):
    """
    Determine the next node to execute based on supervisor's decision.
    """
    if not state.get("approved"):
        # Wait for HITL
        return END 
        
    next_agent = state.get("next_agent")
    
    if next_agent == "ManualQAExpert":
        return "ManualQAExpert"
    elif next_agent == "TestAutomationArchitect":
        return "TestAutomationArchitect"
    elif next_agent == "TestAutomationEngineer":
        return "TestAutomationEngineer"
    elif next_agent == "CodeQualityGate":
        return "CodeQualityGate"
    elif next_agent == "TechnicalWriter":
        return "TechnicalWriter"
    elif next_agent == "FINISH":
        return END
        
    # If no recognized next step, return to supervisor or end
    return END

def create_graph():
    """
    Build the LangGraph StateMachine.
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("Supervisor", entrypoint_node)
    workflow.add_node("ManualQAExpert", manual_qa_node)
    workflow.add_node("TestAutomationArchitect", test_auto_architect_node)
    workflow.add_node("TestAutomationEngineer", test_auto_engineer_node)
    workflow.add_node("CodeQualityGate", code_quality_node)
    workflow.add_node("TechnicalWriter", tech_writer_node)
    
    # Edges
    workflow.set_entry_point("Supervisor")
    
    # Supervisor routes tasks to agents
    workflow.add_conditional_edges(
        "Supervisor",
        route,
        {
            "ManualQAExpert": "ManualQAExpert",
            "TestAutomationArchitect": "TestAutomationArchitect",
            "TestAutomationEngineer": "TestAutomationEngineer",
            "CodeQualityGate": "CodeQualityGate",
            "TechnicalWriter": "TechnicalWriter",
            END: END
        }
    )
    
    # Workers report back to Supervisor
    workflow.add_edge("ManualQAExpert", "Supervisor")
    workflow.add_edge("TestAutomationArchitect", "Supervisor")
    workflow.add_edge("TestAutomationEngineer", "Supervisor")
    workflow.add_edge("CodeQualityGate", "Supervisor")
    workflow.add_edge("TechnicalWriter", "Supervisor")
    
    return workflow.compile()
