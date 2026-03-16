# Configuration

QORE is highly configurable via environment variables and project-level settings. This guide covers everything you need to set up your environment for high-performance orchestration.

## Environment Variables

Create a `.env` file in the project root. You can use `.env.example` as a template.

### LLM Provider
QORE supports multiple LLM providers. Configure your preferred one here:

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai # Options: openai, anthropic, google
MODEL_NAME=gpt-4o   # Recommended: gpt-4o or claude-3-5-sonnet
```

### API Keys
Provide the keys for the services you intend to use:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=ant-python-...
GOOGLE_API_KEY=...
```

### Observability (LangSmith)
To enable world-class tracing and debugging, we recommend using LangSmith:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=qore-production
```

## System Settings

The core system settings are located in `core/config.py`. 

### Checkpointer Configuration
By default, QORE uses a local SQLite database named `checkpoints.sqlite` for state persistence. This can be modified in `server.py`:

```python
DB_PATH = "checkpoints.sqlite"
```

### UI Configuration
The UI connects to the backend via WebSockets. If you change the backend port, ensure you update the WebSocket URI in `ui/app/page.tsx`:

```typescript
const socket = new WebSocket(`ws://localhost:8000/ws/${threadId}`);
```

## Infrastructure Requirements

- **Python:** 3.10 or higher.
- **Node.js:** 18.x or higher (for UI and Docs).
- **SQLite:** Enabled by default in Python.
- **Memory:** 4GB RAM recommended for local development.
