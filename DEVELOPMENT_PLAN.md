# Development Plan: AI Career Growth Navigator

## Phase 1: Foundation & Tooling Architecture
**Goal:** Establish the foundational Python framework, Streamlit UI scaffolding, set up secure configurations, and build out the baseline Model Context Protocol (MCP) tool registrations.
- [ ] Initialize Python environment, `requirements.txt`, and `.env.example`.
- [ ] Build `src/core/config.py` for strictly decoupled security/API handling.
- [ ] Implement `src/tools/mcp_base.py` for standardizing MCP tools.
- [ ] Implement `src/tools/memory_tool.py` and `Memory Agent` for persisting state across Streamlit reruns.
- [ ] Create the basic `src/app.py` UI skeleton with navigation tabs.

## Phase 2: Core Analysis Loop
**Goal:** Ingest user state, perform career skill analytics, and identify growth gaps.
- [ ] Implement `profile_tool.py` and **Profile Analysis Agent**.
- [ ] Implement `skill_gap_tool.py` and **Skill Gap Agent**.
- [ ] Build the "Profile & Goals" UI View in Streamlit (Input Form + Gap Dashboard).

## Phase 3: Action Integration
**Goal:** Translate gaps into actionable roadmaps and practical portfolio work.
- [ ] Implement `roadmap_tool.py` and **Learning Roadmap Agent**.
- [ ] Implement `project_tool.py` and **Project Recommendation Agent**.
- [ ] Build "Roadmaps" and "Projects" UI elements, visualizing tasks dynamically.

## Phase 4: Opportunities and Progress Tracking
**Goal:** Map user to real-world contests and manage completion states.
- [ ] Implement `opportunity_tool.py` and **Opportunity Discovery Agent** (Targeting Kaggle, open source, hackathons).
- [ ] Implement `progress_tool.py` and **Progress Tracking Agent**.
- [ ] Complete the "Dashboard" tracking visuals in Streamlit.
- [ ] Bind all tracking data recursively to the Memory Agent.

## Phase 5: Deployability & Final Polish
**Goal:** Productionize the codebase for the Kaggle Capstone Submission.
- [ ] Create `Dockerfile` tailored for Streamlit port `8501` (or local standard `3000`).
- [ ] Write rigorous in-line documentation and docstrings.
- [ ] Polish `README.md` with explicit deployment guides and architecture recaps.
- [ ] Perform security review ensuring no secrets linger and error handling exists across UI layers.
