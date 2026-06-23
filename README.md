# AI Career Growth Navigator (Production Build)

A production-grade, portfolio-quality AI product that analyzes skill gaps and generates multi-agent learning roadmaps, curated portfolio projects, and tracks real market opportunities (Kaggle, Devpost, GitHub, Open Source, Internships).

---

## 🔥 Features
- **Modern SaaS Dashboard:** Completely redesigned responsive user interface featuring glassmorphism cards, metrics, and a clean professional dark theme inspired by Vercel and Linear.
- **True Multi-Agent Architecture:** Powered by `google-genai` and Gemini 2.5 Flash.
- **Secure Key Management:** Hardened environment variable integration. No exposed inputs.
- **Structured Tools:** Pure MCP-based tool mapping for robust outputs.

## 🤖 The 7-Agent System
1. **Supervisor Agent (`Orchestrator`)**: Coordinates the sequential invocation of the workflow.
2. **Profile Agent**: Extracts target outcomes and current competencies using `ProfileAnalysisTool`.
3. **Skill Gap Agent**: Compares against industry requirements using `SkillGapTool`.
4. **Roadmap Agent**: Maps scheduled curriculum timelines using `RoadmapGenerationTool`.
5. **Project Agent**: Designs comprehensive technical portfolio projects.
6. **Opportunity Agent**: Discovers high-quality real-world programs (Kaggle, Google, Open Source) using Structured Outputs from Gemini.
7. **Memory Agent**: Optionally allows for persistent state tracking across sessions.

---

## 🚀 Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Gemini API Key
echo 'GEMINI_API_KEY="your_api_key_here"' > .env

# 3. Start the application
streamlit run src/app.py
```

## ☁️ Streamlit Cloud Deployment Guide
1. Push this repository to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io).
3. Click **New App** and select your repository.
4. Set the **Main file path** to `src/app.py`.
5. Under **Advanced Settings**, add your `GEMINI_API_KEY` to the **Secrets** section.
6. Click **Deploy**.

## 🐳 Docker / Cloud Run Deployment
The `Dockerfile` is natively designed to be deployed to Google Cloud Run or Docker.
It exposes port **3000** ensuring default server compatibility across hosting regimes.

```bash
docker build -t ai-career-navigator .
docker run -p 3000:3000 -e GEMINI_API_KEY="your_actual_key" ai-career-navigator
```
