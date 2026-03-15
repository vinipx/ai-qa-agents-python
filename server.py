from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import create_graph
from langchain_core.messages import HumanMessage
import uuid

app = FastAPI(title="AI QE Agent Service")

class Query(BaseModel):
    requirement: str
    thread_id: str = str(uuid.uuid4())

@app.post("/execute")
async def execute_qe_workflow(query: Query):
    """
    Triggers the Multi-Agent QE workflow remotely.
    """
    workflow = create_graph()
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=query.requirement)],
        "plan": "",
        "approved": True, # Automatically approve for remote API for now
        "metrics": {},
        "next_agent": "",
        "sender": "User"
    }
    
    try:
        # In a production scenario, you'd use a checkpointer 
        # to handle HITL (Human-in-the-loop) via multiple API calls.
        result = workflow.invoke(initial_state)
        return {
            "status": "success",
            "thread_id": query.thread_id,
            "final_response": result["messages"][-1].content,
            "metrics": result.get("metrics", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
