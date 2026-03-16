# Orchestration & State

Orchestration in QORE is powered by **LangGraph**, a library for building stateful, multi-actor applications with LLMs. This section explains how the "chain of thought" becomes a "graph of action."

## The Global State (`AgentState`)

All agents share a unified state object. This ensures that the Manual QA Expert knows what the Supervisor planned, and the Test Engineer knows what the Architect designed.

```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: str           # The master execution plan
    approved: bool      # HITL approval status
    metrics: dict       # Performance & cost tracking
    next_agent: str     # Routing instruction
    sender: str         # The node that just finished
```

## The Graph Definition

The graph is defined in `graph.py`. It uses a combination of nodes (agents) and conditional edges (routing logic).

### Routing Logic
The `route` function acts as the traffic controller. It checks the `approved` flag and the `next_agent` value to determine the next destination.

```python
async def route(state: AgentState):
    if not state.get("approved"):
        return END # Pause for Human-in-the-Loop
    
    # Logic to return "ManualQAExpert", "TechnicalWriter", etc.
    return state.get("next_agent")
```

## Human-in-the-Loop (HITL)

QORE implements a "Breakpoint" pattern. After the Supervisor generates a plan, the `approved` flag is set to `False`, and the graph returns `END`. 

1.  **State Save:** The `AsyncSqliteSaver` persists the state at the breakpoint.
2.  **User Action:** The user reviews the plan in the UI and clicks **APPROVE SEQUENCE**.
3.  **Resumption:** The UI sends an `approve` action to the backend, which updates the state to `approved: True` and re-triggers the graph.

## Async Event Loop

To maintain a responsive UI, the entire orchestration is asynchronous. 
- **Checkpointers:** Use `AsyncSqliteSaver`.
- **Nodes:** Implemented as `async def`.
- **Streaming:** Events are pushed via `workflow.astream_events`.

This architecture prevents the backend from blocking while waiting for long-running LLM calls, allowing real-time token streaming to the Command Center.
