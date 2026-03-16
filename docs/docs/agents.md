# Specialized Agents

QORE's power lies in its workforce of specialized agents. Each agent is a dedicated LLM-powered node with a specific role, system prompt, and set of responsibilities.

## Agent Design Philosophy

Every agent in QORE follows a standardized design pattern:
1.  **System Persona:** Defines the agent's expertise and tone.
2.  **Context Awareness:** Receives the current `AgentState` and the Supervisor's plan.
3.  **Task Focus:** Operates on a specific subset of the requirement.
4.  **Telemetry:** Automatically tracks execution time, tokens used, and cost.

---

## 01_Supervisor (SDLC Architect)
The brain of the system. It orchestrates the entire lifecycle.
- **Responsibility:** Requirements analysis, plan generation, and routing.
- **State Management:** Decides when to move to the next agent and when to stop for human approval.
- **File:** `agents/entrypoint_agent.py`

## 02_Manual QA Expert
Translates high-level business requirements into detailed manual test cases.
- **Output:** Markdown-formatted test suites with preconditions, steps, and expected results.
- **Focus:** Functional coverage, edge cases, and user experience.
- **File:** `agents/manual_qa_agent.py`

## 03_Test Automation Architect
Designs the high-level strategy for automated testing.
- **Responsibility:** Selecting the right framework (e.g., Pytest, Playwright), defining directory structures, and designing reporting logic.
- **File:** `agents/test_auto_architect_agent.py`

## 04_Test Automation Engineer
The implementation specialist that writes the actual code.
- **Output:** Production-ready Python/Pytest scripts or Javascript/Cypress code.
- **Responsibility:** Script implementation based on the Architect's design.
- **File:** `agents/test_auto_engineer_agent.py`

## 05_Code Quality Gate
A specialized auditor that performs static and semantic analysis on generated code.
- **Responsibility:** Reviewing automation scripts for best practices, security vulnerabilities, and logic flaws.
- **File:** `agents/code_quality_agent.py`

## 06_Technical Writer
Ensures the project is well-documented and ready for handoff.
- **Output:** README updates, API documentation, and implementation guides.
- **File:** `agents/tech_writer_agent.py`

---

## Agent Implementation Example

All worker agents share a common async implementation structure:

```python
@async_track_metrics(agent_name="AgentName")
async def agent_node(state: AgentState, config: RunnableConfig | None = None):
    # 1. Extract context
    # 2. Call LLM with specialized prompt
    # 3. Process output
    # 4. Return state update
```
