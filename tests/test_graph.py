from graph import create_graph
from langchain_core.messages import HumanMessage

def test_graph_execution_first_step():
    """
    Integration test: first step (Planning)
    """
    app = create_graph()
    initial_state = {
        "messages": [HumanMessage(content="test req")],
        "plan": "",
        "approved": False,
        "metrics": {},
        "next_agent": "",
        "sender": "User"
    }
    
    result = app.invoke(initial_state)
    
    assert result["plan"] != ""
    assert result["approved"] is False

def test_graph_execution_flow_to_manual_qa():
    """
    Integration test: flow from approval to ManualQA
    """
    app = create_graph()
    
    # State as if supervisor just finished planning
    state = {
        "messages": [HumanMessage(content="test req")],
        "plan": "Plan 1. ManualQAExpert...",
        "approved": True, # User approved
        "metrics": {},
        "next_agent": "",
        "sender": "User"
    }
    
    # Run the graph
    # This should:
    # 1. Start at Supervisor
    # 2. Supervisor sees approved and routes to ManualQAExpert (sets next_agent="ManualQAExpert")
    # 3. Conditional edge routes to ManualQAExpert
    # 4. ManualQAExpert runs and reports back to Supervisor
    # 5. Supervisor decides next step...
    
    result = app.invoke(state)
    
    # Check that ManualQAExpert was at least triggered
    assert "ManualQAExpert" in result["metrics"]
    
    # Check that all agents in the sequence were triggered
    assert "TestAutomationArchitect" in result["metrics"]
    assert "TestAutomationEngineer" in result["metrics"]
    assert "CodeQualityGate" in result["metrics"]
    assert "TechnicalWriter" in result["metrics"]
    
    # Check that we reached the end of the sequence
    assert result["next_agent"] == "FINISH"
