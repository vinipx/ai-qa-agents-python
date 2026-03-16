import pytest
from agents.entrypoint_agent import entrypoint_node
from agents.manual_qa_agent import manual_qa_node
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_supervisor_creates_plan():
    """
    Unit test for Supervisor to ensure it creates a plan initially.
    """
    state = {
        "messages": [HumanMessage(content="test request")],
        "plan": "",
        "approved": False,
        "metrics": {},
        "next_agent": "",
        "sender": "User"
    }
    
    result = await entrypoint_node(state, {})
    
    assert result["plan"] != ""
    assert "PROPOSED PLAN:" in result["messages"][0].content
    assert result["approved"] is False

@pytest.mark.asyncio
async def test_manual_qa_generates_cases():
    """
    Unit test for Manual QA agent.
    """
    state = {
        "messages": [],
        "plan": "Plan content",
        "approved": True,
        "metrics": {},
        "next_agent": None,
        "sender": "Supervisor"
    }
    
    result = await manual_qa_node(state, {})
    
    assert "TEST CASES:" in result["messages"][0].content
    assert result["sender"] == "ManualQAExpert"
