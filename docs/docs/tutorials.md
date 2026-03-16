# Tutorials

New to QORE? Follow these guides to run your first end-to-end agentic orchestration.

## Running Your First Sequence

1.  **Launch the System:**
    ```bash
    ./run.sh
    ```
2.  **Open the Command Center:**
    Navigate to `http://localhost:3000` in your browser.
3.  **Submit a Requirement:**
    In the **Agentic Stream** input, type: 
    > "Plan and implement a test suite for our REST API's /users/create endpoint."
4.  **Review the Plan:**
    The Supervisor will generate a 5-step plan. Watch the Orchestration map as the Supervisor node pulses.
5.  **Approve:**
    Click the **APPROVE SEQUENCE** button.
6.  **Monitor Progress:**
    Watch the real-time trace as it moves from Manual QA to Tech Writer.
7.  **Access Artifacts:**
    Switch to the **Artifacts** tab. Explore the **Vault Index** to view test cases, code, and documentation.

---

## Navigating the Command Center

### Agentic Stream (Left Panel)
This is your primary communication hub. 
- **Green Badges:** Indicate the agent is currently processing.
- **Monospace Text:** Shows the incremental reasoning (tokens) of the active agent.

### Orchestration Map (Right Panel - Tab 1)
A visual pulse of the system.
- **Glowing White Borders:** Indicate the currently active node.
- **Dimmed Nodes:** Represent completed tasks in the current sequence.
- **Animated Edges:** Show the direction of data flow.

### Vault (Right Panel - Tab 2)
The repository for all QE outputs.
- **Vault Index:** Categorizes artifacts by agent source.
- **Content Viewer:** High-fidelity view of the generated Markdown and Code.
- **Copy Content:** Easily extract artifacts for your target repository.

---

## Troubleshooting

- **No animation in the map?** Check `ui/frontend.log` for WebSocket connection issues.
- **Agent stuck?** Refresh the page. QORE's persistence will resume the sequence exactly where it left off.
- **Logs:** Run `tail -f backend.log` to see internal server events.
