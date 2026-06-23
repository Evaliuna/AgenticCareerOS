import streamlit as st
import os
import sys

# Ensure the root project directory is in the Python path
# This fixes "ModuleNotFoundError: No module named 'src'" when running via Streamlit
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.supervisor import Orchestrator
from src.agents.memory import MemoryAgent

st.set_page_config(page_title="AI Career Growth Navigator", layout="wide")

# Ensure environment safety
api_key = os.environ.get("GEMINI_API_KEY", "")
memory_agent = MemoryAgent()

st.title("🚀 AI Career Growth Navigator")
st.markdown("A structured Multi-Agent pipeline orchestrating career gap analysis and structured roadmaps.")

if not api_key:
    st.warning("⚠️ API Key not found in environment (`GEMINI_API_KEY`).")
    api_key_input = st.text_input("Enter your Gemini API Key:", type="password")
    if api_key_input:
        api_key = api_key_input
        os.environ["GEMINI_API_KEY"] = api_key

tab1, tab2, tab3 = st.tabs(["Profile & Goals", "Roadmap & Ops", "Memory Dashboard"])

# --- TAB 1: Inputs ---
with tab1:
    st.header("1. Your Current State")
    skills_input = st.text_area("List your current skills (e.g., Python, React, Basic SQL):", height=100)
    goal_input = st.text_input("What is your target role? (e.g., Senior Data Scientist)")
    
    if st.button("Generate Career Pipeline", type="primary"):
        if not api_key:
            st.error("API Key required to run the agent sequence.")
        elif not skills_input or not goal_input:
            st.error("Please fill out both inputs.")
        else:
            with st.spinner("Multi-Agent System is generating your career pipeline..."):
                orchestrator = Orchestrator(api_key=api_key)
                try:
                    results = orchestrator.run_career_analysis(skills_input, goal_input)
                    st.success("Pipeline Processed Successfully! Proceed to Roadmap tab.")
                    st.session_state["results"] = results
                except Exception as e:
                    st.error(f"Error during agent execution: {e}")

# --- TAB 2: Dashboards ---
if "results" in st.session_state:
    res = st.session_state["results"]
    with tab2:
        st.header("2. Your Gap & Roadmap")
        
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.subheader("Skill Gap Analysis")
            gap_data = res.get("gap_context", {}).get("gap_analysis", {})
            st.write(f"**Missing Tools/Paradigms:** {', '.join(gap_data.get('missing_skills', []))}")
            st.write(f"**Overlapping Skills:** {', '.join(gap_data.get('existing_relevant_skills', []))}")
            st.progress(min(1.0, gap_data.get('gap_percentage', 0) / 100))
            st.caption(f"Gap Percentage: {gap_data.get('gap_percentage', 0)}%")
            
        with col2:
            st.subheader("Learning Roadmap (Structured)")
            weekly = res.get("roadmap_context", {}).get("weekly_schedule", {})
            if weekly:
                for week, skills in weekly.items():
                    with st.expander(f"{week.replace('_', ' ')}"):
                        for s in skills:
                            st.write(f"- {s}")
            else:
                st.write("No schedule generated.")
            
            # --- FEEDBACK LOOP ---
            st.write("---")
            feedback = st.text_input("Feedback on Roadmap? (e.g., 'I only have 2 hours a week')")
            if st.button("Adapt Roadmap"):
                with st.spinner("Adapting Roadmap..."):
                    orchestrator = Orchestrator(api_key=api_key)
                    new_res = orchestrator.adapt_roadmap(feedback, st.session_state["results"])
                    st.session_state["results"] = new_res
                    st.rerun()

        st.divider()
        
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Custom Portfolio Project")
            proj = res.get("project_context", {})
            if "title" in proj:
                st.info(f"### {proj['title']}\\n**Stack:** {', '.join(proj.get('stack', []))}\\n**Difficulty:** {proj.get('difficulty')}\\n\\n{proj.get('description')}")
            elif "error" in proj:
                st.error(f"Project Agent Error: {proj['error']}")
                
        with col4:
            st.subheader("Live OS Opportunities (GitHub API)")
            opps = res.get("opportunities_context", {}).get("opportunities_found", [])
            if opps:
                for o in opps:
                    st.success(f"**{o.get('type')}**: [{o.get('name')}]({o.get('url')})")
            elif res.get("opportunities_context", {}).get("error"):
                 st.error(res.get("opportunities_context", {}).get("error"))
            else:
                st.write("No live opportunities found for this query.")

# --- TAB 3: Memory ---
with tab3:
    st.header("State Memory & Persistence")
    st.write("This application retains state via the Native File Memory Tool (JSON RPC analog).")
    
    colA, colB = st.columns(2)
    with colA:
        if st.button("Load Saved Memory"):
            state = memory_agent.load_state()
            st.json(state)
            
    with colB:
        if st.button("Clear Long-Term Memory"):
            memory_agent.clear_state()
            st.session_state.pop("results", None)
            st.success("Memory purged successfully.")

