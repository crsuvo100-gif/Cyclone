# Cyclone — PROJECT PLAN

## Project Overview
- **Project Name:** Cyclone.0 (MOON V13.0 Extension)
- **Project Root:** /home/meow/Projects/MOON/Cyclone
- **Type:** Local-first AI terminal ecosystem (Python backend + Node.js frontend + Voice + Agent connectors)
- **Status:** IN PROGRESS

## Milestones
1. [ ] Milestone 1: Project Discovery & Audit (COMPLETE)
2. [ ] Milestone 2: Persistent State Setup (COMPLETE)
3. [ ] Milestone 3: Multi-agent Developer System (IN PROGRESS)
4. [ ] Milestone 4: Advanced Reasoning & Knowledge Engine
5. [ ] Milestone 5: Voice & Multimodal Intelligence
6. [ ] Milestone 6: Security, Observability & Recovery
7. [ ] Milestone 7: UI/UX Redesign (Holographic)
8. [ ] Milestone 8: GitHub Delivery Setup

## Architecture
- **Backend:** Python 3.10+, FastAPI, Ollama (25 models)
- **Frontend:** Node.js HTTP server (CYCLONE V10), vanilla HTML/CSS/JS
- **Voice:** Female voice clone (alice.wav), espeak + SoX
- **Agents:** Planner, Architect, Implementer, Reviewer
- **Memory:** Long-term (SQLite) + Short-term + Working memory + Episodic
- **Connectors:** moon_local, apidog, cyclone

## Technology Stack
- Python 3.10+
- FastAPI + Uvicorn
- Node.js 18+
- SQLite (memory db)
- Ollama (local models)
- espeak + SoX (voice)
- VS Code (development)

## Key Files
- main.py - MOON-AI CLI entrypoint
- server.js - Node.js CYCLONE server
- app/cyclone.py - Cyclone app module
- app/orchestrator.py - Main brain orchestrator
- apps/moon_ui/hud.html - MOON neural core HUD
- apps/cyclone/index.html - Cyclone terminal UI

## Next Steps
1. Verify backend health (python -m moon doctor)
2. Start CYCLONE server (npm start)
3. Test browser UI at localhost:8765
4. Implement Phase 1: Universal Agent Connector + HERMES Integration
5. Implement Phase 2: Browser + Computer Use + Advanced Research
6. Implement Phase 3: Coding + File + Data Intelligence
7. Implement Phase 4: Voice + Vision + Multimodal
8. Implement Phase 5: Security + Observability + Evaluation + Recovery

## Backup Strategy
- Local: /home/meow/backup-YYYYMMDD-HHMMSS.tar.gz
- Reports: /home/meow/Project-Reports/Cyclone/
