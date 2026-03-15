import json
from graph import create_graph
from langchain_core.messages import HumanMessage

def print_messages(messages):
    for m in messages:
        print(f"[{m.type.capitalize()}]: {m.content}")
        print("-" * 40)

def main():
    print("Initializing Multi-Agent QE Framework...")
    app = create_graph()
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content="Create a test suite for the new login API.")],
        "plan": "",
        "approved": False,
        "metrics": {},
        "next_agent": "",
        "sender": "User"
    }

    print("\n--- Phase 1: Planning (Supervisor) ---")
    # First execution to get the plan
    result = app.invoke(initial_state)
    print_messages(result["messages"])
    
    # Extract the plan and ask for approval (HITL)
    plan = result["plan"]
    print(f"\nSupervisor generated plan:\n{plan}\n")
    approval = input("Do you approve this plan? (yes/no): ").strip().lower()
    
    if approval == 'yes':
        print("\n--- Phase 2: Execution (Routing to Agents) ---")
        # Update state with approval and continue execution
        result["approved"] = True
        
        # In a real LangGraph setup with checkpointer, we would update state. 
        # Here we just pass the updated dictionary to invoke again.
        # Note: LangGraph naturally continues if state is updated and run again 
        # but the simplest mockup passes the new state.
        final_result = app.invoke(result)
        
        print("\n--- Execution Finished ---")
        print_messages(final_result["messages"])
        print("\n--- Telemetry Metrics ---")
        print(json.dumps(final_result.get("metrics", {}), indent=2))
        
        print("\nRaising Pull Request with changes... (Mocked)")
    else:
        print("\nPlan rejected. Aborting execution.")

if __name__ == "__main__":
    main()
