from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import compile_graph
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import uuid
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QORE_API")

app = FastAPI(title="QORE Agent Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "checkpoints.sqlite"

class Query(BaseModel):
    requirement: str
    thread_id: str = str(uuid.uuid4())

@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    await websocket.accept()
    logger.info(f"WS Connected: {thread_id}")
    
    try:
        async with AsyncSqliteSaver.from_conn_string(DB_PATH) as memory:
            workflow = compile_graph(checkpointer=memory)
            config = {"configurable": {"thread_id": thread_id}}
            
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                action = message_data.get("action", "prompt")
                requirement = message_data.get("requirement", "")

                # Get current state from checkpoint
                state_snapshot = await workflow.aget_state(config)
                current_values = state_snapshot.values if state_snapshot else {}

                # Prepare the "kick" payload to restart the graph
                payload = {}

                if action == "approve":
                    logger.info(f"Action: APPROVE for {thread_id}")
                    payload = {
                        "approved": True, 
                        "messages": [SystemMessage(content="User approved the plan.")],
                        "sender": "User"
                    }
                else:
                    logger.info(f"Action: PROMPT for {thread_id}")
                    if not requirement:
                        continue
                    
                    payload = {
                        "messages": [HumanMessage(content=requirement)],
                        "sender": "User",
                        "approved": True # Initial prompts are auto-approved to let supervisor plan
                    }
                    
                    # Fresh thread initialization
                    if not current_values.get("plan"):
                        payload.update({
                            "plan": "",
                            "metrics": {},
                            "next_agent": ""
                        })

                # STREAM: Passing the payload directly to astream_events RE-TRIGGERS the graph
                async for event in workflow.astream_events(payload, config=config, version="v1"):
                    kind = event["event"]
                    
                    if kind == "on_chat_model_stream":
                        content = event["data"]["chunk"].content
                        if content:
                            await websocket.send_json({
                                "type": "token", 
                                "content": content, 
                                "node": event["metadata"].get("langgraph_node", "unknown")
                            })
                    
                    elif kind == "on_chain_start":
                        node_name = event["metadata"].get("langgraph_node")
                        if node_name:
                            await websocket.send_json({"type": "node_start", "node": node_name})
                    
                    elif kind == "on_chain_end":
                        node_name = event["metadata"].get("langgraph_node")
                        if node_name:
                            res = event["data"].get("output", {})
                            display_output = ""
                            # If it's a node output, extract the last message for the Artifacts UI
                            if isinstance(res, dict) and "messages" in res and res["messages"]:
                                display_output = res["messages"][-1].content
                            
                            await websocket.send_json({
                                "type": "node_end", 
                                "node": node_name, 
                                "output": display_output
                            })
                
                # FINAL SNAPSHOT: Send the latest state to sync UI
                state_data = await workflow.aget_state(config)
                final_values = state_data.values
                
                await websocket.send_json({
                    "type": "final",
                    "content": final_values["messages"][-1].content,
                    "metrics": final_values.get("metrics", {}),
                    "approved": final_values.get("approved", False),
                    "plan": final_values.get("plan", "")
                })

    except WebSocketDisconnect:
        logger.info(f"WS Disconnected: {thread_id}")
    except Exception as e:
        logger.error(f"Error in WS loop: {str(e)}", exc_info=True)
        try:
            await websocket.send_json({"type": "error", "content": f"SYSTEM_ERR: {str(e)}"})
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
