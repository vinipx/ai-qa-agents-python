#!/usr/bin/env bash

# QORE - Local Runner
# Professional startup script for Backend, Frontend, and Documentation

# Colors for professional logging
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${CYAN}             QORE - STARTING ECOSYSTEM                     ${NC}"
echo -e "${BLUE}============================================================${NC}"

# 1. Environment & Tool Checks
echo -e "${BLUE}[1/6] Checking prerequisites...${NC}"
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo -e "${RED}❌ Error: Python not found. Please install Python 3.10+.${NC}"
    exit 1
fi
if ! command -v node &>/dev/null; then
    echo -e "${RED}❌ Error: Node.js not found. Please install Node.js 18+.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Environment tools detected.${NC}"

# 2. Cleanup existing processes
echo -e "${BLUE}[2/6] Cleaning up stale sessions...${NC}"
lsof -ti :8000,3000,3001 | xargs kill -9 2>/dev/null || true
sleep 2
echo -e "${GREEN}✅ Ports cleared.${NC}"

# 3. Python Setup
echo -e "${BLUE}[3/6] Synchronizing Python dependencies...${NC}"
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then python3 -m venv $VENV_DIR; fi
if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then source $VENV_DIR/bin/activate
else source $VENV_DIR/Scripts/activate; fi
pip install -e . --quiet
pip install langgraph-checkpoint-sqlite aiosqlite "uvicorn[standard]" --quiet
echo -e "${GREEN}✅ Python environment ready.${NC}"

# 4. JS Setup
echo -e "${BLUE}[4/6] Synchronizing JS dependencies...${NC}"
(cd ui && npm install --silent)
(cd docs && npm install --silent && npm run clear -- --quiet 2>/dev/null || true)
echo -e "${GREEN}✅ JS environments ready.${NC}"

# 5. Configuration Check
if [ ! -f ".env" ]; then cp .env.example .env; fi

# 6. Launch Ecosystem
echo -e "${BLUE}[6/6] Launching services...${NC}"
trap "kill 0" EXIT

echo -e "${CYAN}🚀 Starting API Backend on http://localhost:8000...${NC}"
python server.py > backend.log 2>&1 &

echo -e "${CYAN}🚀 Starting UI Frontend on http://localhost:3000...${NC}"
(cd ui && npm run dev > frontend.log 2>&1) &

echo -e "${CYAN}🚀 Starting Documentation on http://localhost:3001...${NC}"
# Use 'localhost' consistently for server and check
(cd docs && npm start -- --port 3001 --host localhost > ../docs.log 2>&1) &

echo -e "${CYAN}⏳ Initializing telemetry and protocols...${NC}"
sleep 5 # Head start for Docusaurus

# Improved Wait Loop: Check for actual connectivity
MAX_RETRIES=120 
COUNT=0
while ! curl -s http://localhost:3001/ >/dev/null; do
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo -e "${RED}⚠️  Timeout: Documentation failed to respond at http://localhost:3001/ after ${MAX_RETRIES}s.${NC}"
        break
    fi
    sleep 1
    ((COUNT++))
    if [ $((COUNT % 10)) -eq 0 ]; then
        echo -e "${BLUE}...still establishing protocol links ($COUNT/$MAX_RETRIES s)...${NC}"
    fi
done

echo -e "${BLUE}============================================================${NC}"
if curl -s http://localhost:3001/ >/dev/null; then
    echo -e "${GREEN}✨ QORE ECOSYSTEM ONLINE!${NC}"
else
    echo -e "${RED}❌ Warning: Documentation service unresponsive. Check docs.log.${NC}"
fi

echo -e "${BLUE}============================================================${NC}"
echo -e "🔗 APP:  ${CYAN}http://localhost:3000${NC}"
echo -e "🔗 DOCS: ${CYAN}http://localhost:3001/${NC}"
echo -e "🔗 API:  ${CYAN}http://localhost:8000${NC}"
echo -e "📖 Logs: ${BLUE}Backend: backend.log | UI: ui/frontend.log | Docs: docs.log${NC}"
echo -e "${BLUE}============================================================${NC}"

wait
